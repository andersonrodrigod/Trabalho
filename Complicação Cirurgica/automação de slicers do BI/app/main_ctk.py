from __future__ import annotations

from datetime import datetime
import shutil
import threading
from pathlib import Path
import sys
from tkinter import filedialog, messagebox

import customtkinter as ctk

# Permite executar este arquivo diretamente (python app/main_ctk.py)
# sem perder o import do pacote "core".
if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.config import PipelineConfig
from core.pipeline import executar_pipeline


class ExecutorApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Executor de Slides BI")
        self.geometry("900x560")

        if getattr(sys, "frozen", False):
            self.base_dir = Path(sys.executable).resolve().parent
            self.bundle_dir = Path(getattr(sys, "_MEIPASS", self.base_dir))
        else:
            self.base_dir = Path(__file__).resolve().parent.parent
            self.bundle_dir = self.base_dir

        self.assets_dir = self.bundle_dir / "assets"
        self.input_path: Path | None = None

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.label_titulo = ctk.CTkLabel(
            self,
            text="Automacao de Slides",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.label_titulo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.frame_entrada = ctk.CTkFrame(self)
        self.frame_entrada.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.frame_entrada.grid_columnconfigure(1, weight=1)

        self.btn_input = ctk.CTkButton(
            self.frame_entrada,
            text="Selecionar Arquivo de Entrada",
            command=self.selecionar_arquivo_entrada,
            width=260,
            height=42,
        )
        self.btn_input.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        self.label_input = ctk.CTkLabel(
            self.frame_entrada,
            text="Nenhum arquivo selecionado",
            anchor="w",
        )
        self.label_input.grid(row=0, column=1, padx=(6, 12), pady=12, sticky="ew")

        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.frame_botoes.grid_columnconfigure((0, 1), weight=1)

        self.btn_totais = ctk.CTkButton(
            self.frame_botoes,
            text="GERAR SLIDE DAS CIRURGIAS GERAIS",
            command=lambda: self.executar_pipeline_ui(
                nome_saida="cirurgias_gerais",
                tipo_filtro=None,
                descricao="CIRURGIAS GERAIS",
            ),
            height=42,
        )
        self.btn_totais.grid(row=0, column=0, padx=10, pady=15, sticky="ew")

        self.btn_tipo = ctk.CTkButton(
            self.frame_botoes,
            text="GERAR SLIDES DAS CIRURGIAS DE VIDEO ABDOMINAL",
            command=lambda: self.executar_pipeline_ui(
                nome_saida="video_abdominal",
                tipo_filtro="VIDEO ABDOMINAL",
                descricao="VIDEO ABDOMINAL",
            ),
            height=42,
        )
        self.btn_tipo.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        self.frame_botoes.grid_remove()

        self.frame_status = ctk.CTkFrame(self)
        self.frame_status.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.frame_status.grid_columnconfigure(0, weight=1)

        self.label_status = ctk.CTkLabel(self.frame_status, text="Aguardando execucao")
        self.label_status.grid(row=0, column=0, padx=12, pady=(10, 6), sticky="w")

        self.progress = ctk.CTkProgressBar(self.frame_status)
        self.progress.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="ew")
        self.progress.set(0)

        self.log_box = ctk.CTkTextbox(self, wrap="word")
        self.log_box.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.log_box.insert("1.0", "Selecione um arquivo de entrada para continuar.\n")
        self.log_box.configure(state="disabled")

    def selecionar_arquivo_entrada(self) -> None:
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo Excel de entrada",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls"), ("Todos os arquivos", "*.*")],
        )
        if not arquivo:
            return

        self.input_path = Path(arquivo)
        self.label_input.configure(text=str(self.input_path))
        self.frame_botoes.grid()
        self.append_log(f"Arquivo selecionado: {self.input_path}")

    def set_botoes_habilitados(self, habilitado: bool) -> None:
        estado = "normal" if habilitado else "disabled"
        self.btn_input.configure(state=estado)
        self.btn_totais.configure(state=estado)
        self.btn_tipo.configure(state=estado)

    def append_log(self, texto: str) -> None:
        self.log_box.configure(state="normal")
        self.log_box.insert("end", texto + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def executar_pipeline_ui(self, nome_saida: str, tipo_filtro: str | None, descricao: str) -> None:
        if self.input_path is None:
            messagebox.showwarning("Arquivo de entrada", "Selecione primeiro o arquivo de entrada.")
            return

        self.set_botoes_habilitados(False)
        self.append_log(f"Iniciando geracao: {descricao}")
        self.atualizar_status(0.0, "Iniciando...")
        thread = threading.Thread(
            target=self._rodar_pipeline,
            args=(nome_saida, tipo_filtro, descricao),
            daemon=True,
        )
        thread.start()

    def _rodar_pipeline(self, nome_saida: str, tipo_filtro: str | None, descricao: str) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pasta_saida_exec = self.base_dir / "data" / "output" / f"{nome_saida}_{timestamp}"
        layout_mode = "grid4" if tipo_filtro == "VIDEO ABDOMINAL" else "paired"
        config = PipelineConfig(
            nome=nome_saida,
            arquivo_entrada=self.input_path if self.input_path else Path(),
            pasta_saida=pasta_saida_exec,
            tipo_filtro=tipo_filtro,
            layout_mode=layout_mode,
        )
        try:
            def progress_cb(valor: float, mensagem: str) -> None:
                self.after(0, self.atualizar_status, valor, mensagem)
                self.after(0, self.append_log, mensagem)

            saidas = executar_pipeline(
                config=config,
                assets_dir=self.assets_dir,
                progress_callback=progress_cb,
            )
            self.after(0, self._salvar_arquivos_finais, descricao, saidas)
        except Exception as exc:
            self.after(0, self.append_log, f"Excecao: {exc}\n")
            self.after(0, messagebox.showerror, "Falha na geracao", str(exc))
        finally:
            self.after(0, self.set_botoes_habilitados, True)

    def _salvar_arquivos_finais(self, descricao: str, saidas: dict[str, Path]) -> None:
        self.append_log("Geracao concluida. Selecione a pasta para salvar os arquivos finais.")
        self.atualizar_status(1.0, "Pipeline concluido. Aguardando pasta de destino")
        pasta_destino = filedialog.askdirectory(title="Escolha a pasta para salvar os arquivos")
        if not pasta_destino:
            self.append_log("Salvamento cancelado pelo usuario.\n")
            self.atualizar_status(1.0, "Concluido sem copiar arquivos")
            return

        destino_base = Path(pasta_destino) / descricao.lower().replace(" ", "_")
        destino_base.mkdir(parents=True, exist_ok=True)

        for origem in saidas.values():
            shutil.copy2(origem, destino_base / origem.name)

        self.append_log(f"Arquivos salvos em: {destino_base}\n")
        self.atualizar_status(1.0, "Concluido com sucesso")

    def atualizar_status(self, progresso: float, mensagem: str) -> None:
        progresso = max(0.0, min(1.0, progresso))
        self.progress.set(progresso)
        self.label_status.configure(text=f"{int(progresso * 100)}% - {mensagem}")


def main() -> None:
    app = ExecutorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
