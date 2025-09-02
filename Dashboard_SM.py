import pandas as pd
from typing import Dict
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import logging
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime
import sys
import os

# Adicionar o caminho para importar classes do dashboard
sys.path.append(os.path.join(os.path.dirname(__file__), 'DashboardSM', 'Class', 'src'))

# Classe SSAVisualizer será definida abaixo como fallback


class SimpleSSAVisualizer:
    """Visualizador simplificado para SSAs quando a classe completa não está disponível."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def create_status_chart(self):
        """Cria gráfico de status das SSAs."""
        if len(self.df) == 0:
            return go.Figure()

        # Contagem por status (usando coluna genérica se SSAColumns não estiver disponível)
        try:
            status_counts = self.df.iloc[:, 1].value_counts()  # Assumindo coluna 1 como status
        except:
            status_counts = pd.Series({"Dados não disponíveis": len(self.df)})

        fig = go.Figure(data=[
            go.Bar(x=status_counts.index, y=status_counts.values)
        ])
        fig.update_layout(
            title="Status das SSAs",
            xaxis_title="Status",
            yaxis_title="Quantidade"
        )
        return fig

    def create_priority_chart(self):
        """Cria gráfico de prioridade das SSAs."""
        if len(self.df) == 0:
            return go.Figure()

        try:
            priority_counts = self.df.iloc[:, 12].value_counts()  # Assumindo coluna 12 como prioridade
        except:
            priority_counts = pd.Series({"Dados não disponíveis": len(self.df)})

        fig = go.Figure(data=[
            go.Pie(labels=priority_counts.index, values=priority_counts.values)
        ])
        fig.update_layout(title="Distribuição por Prioridade")
        return fig


# Usar a classe disponível ou o fallback
SSAVisualizer = SimpleSSAVisualizer  # Usar sempre o fallback simplificado por enquanto


@dataclass
class SSAData:
    """Estrutura de dados para uma SSA."""

    numero: str
    situacao: str
    derivada: Optional[str]
    localizacao: str
    desc_localizacao: str
    equipamento: str
    semana_cadastro: str
    emitida_em: datetime
    descricao: str
    setor_emissor: str
    setor_executor: str
    solicitante: str
    servico_origem: str
    prioridade_emissao: str
    prioridade_planejamento: Optional[str]
    execucao_simples: str
    responsavel_programacao: Optional[str]
    semana_programada: Optional[str]
    responsavel_execucao: Optional[str]
    descricao_execucao: Optional[str]
    sistema_origem: str
    anomalia: Optional[str]

    def to_dict(self) -> Dict:
        """Converte o objeto para dicionário."""
        return {
            "numero": self.numero,
            "situacao": self.situacao,
            "setor_executor": self.setor_executor,
            "prioridade": self.prioridade_emissao,
            "emitida_em": (
                self.emitida_em.strftime("%Y-%m-%d %H:%M:%S")
                if self.emitida_em
                else None
            ),
        }


class SSAColumns:
    """Mantém os índices e nomes das colunas."""

    # Índices
    NUMERO_SSA = 0
    SITUACAO = 1
    DERIVADA = 2
    LOCALIZACAO = 3
    DESC_LOCALIZACAO = 4
    EQUIPAMENTO = 5
    SEMANA_CADASTRO = 6
    EMITIDA_EM = 7
    DESC_SSA = 8
    SETOR_EMISSOR = 9
    SETOR_EXECUTOR = 10
    SOLICITANTE = 11
    SERVICO_ORIGEM = 12
    GRAU_PRIORIDADE_EMISSAO = 13
    GRAU_PRIORIDADE_PLANEJAMENTO = 14
    EXECUCAO_SIMPLES = 15
    RESPONSAVEL_PROGRAMACAO = 16
    SEMANA_PROGRAMADA = 17
    RESPONSAVEL_EXECUCAO = 18
    DESCRICAO_EXECUCAO = 19
    SISTEMA_ORIGEM = 20
    ANOMALIA = 21

    # Nomes para exibição
    COLUMN_NAMES = {
        NUMERO_SSA: "Número da SSA",
        SITUACAO: "Situação",
        DERIVADA: "Derivada de",
        LOCALIZACAO: "Localização",
        DESC_LOCALIZACAO: "Descrição da Localização",
        EQUIPAMENTO: "Equipamento",
        SEMANA_CADASTRO: "Semana de Cadastro",
        EMITIDA_EM: "Emitida Em",
        DESC_SSA: "Descrição da SSA",
        SETOR_EMISSOR: "Setor Emissor",
        SETOR_EXECUTOR: "Setor Executor",
        SOLICITANTE: "Solicitante",
        SERVICO_ORIGEM: "Serviço de Origem",
        GRAU_PRIORIDADE_EMISSAO: "Grau de Prioridade Emissão",
        GRAU_PRIORIDADE_PLANEJAMENTO: "Grau de Prioridade Planejamento",
        EXECUCAO_SIMPLES: "Execução Simples",
        RESPONSAVEL_PROGRAMACAO: "Responsável na Programação",
        SEMANA_PROGRAMADA: "Semana Programada",
        RESPONSAVEL_EXECUCAO: "Responsável na Execução",
        DESCRICAO_EXECUCAO: "Descrição Execução",
        SISTEMA_ORIGEM: "Sistema de Origem",
        ANOMALIA: "Anomalia",
    }

    @classmethod
    def get_name(cls, index: int) -> str:
        """Retorna o nome da coluna pelo índice."""
        return cls.COLUMN_NAMES.get(index, f"Coluna {index}")


class SSADashboard:
    """Dashboard interativo para análise de SSAs."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.visualizer = SSAVisualizer(df)
        self.kpi_calc = KPICalculator(df)
        self.setup_layout()
        self.setup_callbacks()

    def _get_state_counts(self):
        """Obtém contagem de SSAs por estado."""
        return self.df.iloc[:, SSAColumns.SITUACAO].value_counts().to_dict()

    def _get_programmed_by_week(self):
        """Obtém SSAs programadas por semana."""
        return self.df.iloc[:, SSAColumns.SEMANA_PROGRAMADA].value_counts().sort_index()

    def _get_responsaveis(self):
        """Obtém lista de responsáveis únicos."""
        prog = self.df.iloc[:, SSAColumns.RESPONSAVEL_PROGRAMACAO].unique()
        exec_ = self.df.iloc[:, SSAColumns.RESPONSAVEL_EXECUCAO].unique()
        return {
            "programacao": sorted([x for x in prog if pd.notna(x) and x != ""]),
            "execucao": sorted([x for x in exec_ if pd.notna(x) and x != ""]),
        }

    def setup_layout(self):
        """Define o layout do dashboard."""
        stats = self._get_initial_stats()
        state_counts = self._get_state_counts()

        self.app.layout = dbc.Container(
            [
                # Header
                dbc.Row(
                    [
                        dbc.Col(
                            html.H1("Dashboard de SSAs", className="text-primary mb-4"),
                            width=12,
                        )
                    ]
                ),
                # Filtros
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Responsável Programação:"),
                                dcc.Dropdown(
                                    id="resp-prog-filter",
                                    options=[
                                        {"label": resp, "value": resp}
                                        for resp in self._get_responsaveis()[
                                            "programacao"
                                        ]
                                    ],
                                    placeholder="Selecione um responsável...",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                html.Label("Responsável Execução:"),
                                dcc.Dropdown(
                                    id="resp-exec-filter",
                                    options=[
                                        {"label": resp, "value": resp}
                                        for resp in self._get_responsaveis()["execucao"]
                                    ],
                                    placeholder="Selecione um responsável...",
                                ),
                            ],
                            width=6,
                        ),
                    ],
                    className="mb-4",
                ),
                # Cards de Estado
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4("SSAs por Estado", className="mb-3"),
                                self._create_state_cards(state_counts),
                            ],
                            width=12,
                        )
                    ],
                    className="mb-4",
                ),
                # Gráficos
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            "SSAs por Responsável na Programação"
                                        ),
                                        dbc.CardBody(dcc.Graph(id="resp-prog-chart")),
                                    ],
                                )
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            "SSAs por Responsável na Execução"
                                        ),
                                        dbc.CardBody(dcc.Graph(id="resp-exec-chart")),
                                    ],
                                )
                            ],
                            width=6,
                        ),
                    ],
                    className="mb-4",
                ),
                # Gráfico de SSAs programadas por semana
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("SSAs Programadas por Semana"),
                                        dbc.CardBody(dcc.Graph(id="week-chart")),
                                    ],
                                )
                            ],
                            width=12,
                        )
                    ],
                    className="mb-4",
                ),
                # Seção de detalhamento (visível apenas quando um responsável é selecionado)
                html.Div(
                    [
                        html.H4("Detalhamento por Responsável", className="mb-3"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    "SSAs Pendentes por Estado"
                                                ),
                                                dbc.CardBody(
                                                    dcc.Graph(id="detail-state-chart")
                                                ),
                                            ],
                                        )
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    "SSAs Programadas por Semana"
                                                ),
                                                dbc.CardBody(
                                                    dcc.Graph(id="detail-week-chart")
                                                ),
                                            ],
                                        )
                                    ],
                                    width=6,
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                    id="detail-section",
                    style={"display": "none"},
                ),
                # Tabela de SSAs
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Lista de SSAs"),
                                        dbc.CardBody(
                                            dash_table.DataTable(
                                                id="ssa-table",
                                                columns=[
                                                    {"name": "Número", "id": "numero"},
                                                    {"name": "Estado", "id": "estado"},
                                                    {
                                                        "name": "Resp. Prog.",
                                                        "id": "resp_prog",
                                                    },
                                                    {
                                                        "name": "Resp. Exec.",
                                                        "id": "resp_exec",
                                                    },
                                                    {
                                                        "name": "Semana Prog.",
                                                        "id": "semana_prog",
                                                    },
                                                    {
                                                        "name": "Prioridade",
                                                        "id": "prioridade",
                                                    },
                                                ],
                                                data=self._prepare_table_data(),
                                                page_size=10,
                                                style_table={"overflowX": "auto"},
                                                style_cell={"textAlign": "left"},
                                                style_header={
                                                    "backgroundColor": "rgb(230, 230, 230)",
                                                    "fontWeight": "bold",
                                                },
                                            )
                                        ),
                                    ],
                                )
                            ],
                            width=12,
                        )
                    ]
                ),
            ],
            fluid=True,
            className="p-4",
        )

    def _create_state_cards(self, state_counts):
        """Cria cards para cada estado de SSA."""
        cards = []
        for state, count in state_counts.items():
            cards.append(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6(state, className="card-title text-center"),
                                    html.H3(
                                        str(count), className="text-center text-primary"
                                    ),
                                ]
                            )
                        ],
                        className="mb-3",
                        style={"height": "100px"},  # Altura fixa para uniformidade
                    ),
                    width=2,
                )
            )
        return dbc.Row(cards)

    def _prepare_table_data(self):
        """Prepara dados para a tabela."""
        table_data = []
        for idx, row in self.df.iterrows():
            try:
                # Garantir que os valores sejam do tipo correto para dash_table
                numero = str(row.iloc[SSAColumns.NUMERO_SSA]) if pd.notna(row.iloc[SSAColumns.NUMERO_SSA]) else ""
                estado = str(row.iloc[SSAColumns.SITUACAO]) if pd.notna(row.iloc[SSAColumns.SITUACAO]) else ""
                resp_prog = str(row.iloc[SSAColumns.RESPONSAVEL_PROGRAMACAO]) if pd.notna(row.iloc[SSAColumns.RESPONSAVEL_PROGRAMACAO]) else ""
                resp_exec = str(row.iloc[SSAColumns.RESPONSAVEL_EXECUCAO]) if pd.notna(row.iloc[SSAColumns.RESPONSAVEL_EXECUCAO]) else ""
                semana_prog = str(row.iloc[SSAColumns.SEMANA_PROGRAMADA]) if pd.notna(row.iloc[SSAColumns.SEMANA_PROGRAMADA]) else ""
                prioridade = str(row.iloc[SSAColumns.GRAU_PRIORIDADE_EMISSAO]) if pd.notna(row.iloc[SSAColumns.GRAU_PRIORIDADE_EMISSAO]) else ""

                table_data.append({
                    "numero": numero,
                    "estado": estado,
                    "resp_prog": resp_prog,
                    "resp_exec": resp_exec,
                    "semana_prog": semana_prog,
                    "prioridade": prioridade,
                })
            except (IndexError, KeyError):
                # Se houver erro ao acessar as colunas, pular esta linha
                continue

        return table_data

    def setup_callbacks(self):
        """Configura os callbacks para interatividade."""

        @self.app.callback(
            [
                Output("resp-prog-chart", "figure"),
                Output("resp-exec-chart", "figure"),
                Output("week-chart", "figure"),
                Output("detail-section", "style"),
                Output("detail-state-chart", "figure"),
                Output("detail-week-chart", "figure"),
                Output("ssa-table", "data"),
            ],
            [Input("resp-prog-filter", "value"), Input("resp-exec-filter", "value")],
        )
        def update_all_charts(resp_prog, resp_exec):
            # Filtra o DataFrame baseado nos responsáveis selecionados
            df_filtered = self.df.copy()
            if resp_prog:
                df_filtered = df_filtered[
                    df_filtered.iloc[:, SSAColumns.RESPONSAVEL_PROGRAMACAO] == resp_prog
                ]
            if resp_exec:
                df_filtered = df_filtered[
                    df_filtered.iloc[:, SSAColumns.RESPONSAVEL_EXECUCAO] == resp_exec
                ]

            # Gráfico de responsáveis na programação
            resp_prog_counts = df_filtered.iloc[
                :, SSAColumns.RESPONSAVEL_PROGRAMACAO
            ].value_counts()
            fig_prog = go.Figure(
                data=[go.Bar(x=resp_prog_counts.index, y=resp_prog_counts.values)]
            )
            fig_prog.update_layout(
                title="SSAs por Responsável na Programação",
                xaxis_title="Responsável",
                yaxis_title="Quantidade",
            )

            # Gráfico de responsáveis na execução
            resp_exec_counts = df_filtered.iloc[
                :, SSAColumns.RESPONSAVEL_EXECUCAO
            ].value_counts()
            fig_exec = go.Figure(
                data=[go.Bar(x=resp_exec_counts.index, y=resp_exec_counts.values)]
            )
            fig_exec.update_layout(
                title="SSAs por Responsável na Execução",
                xaxis_title="Responsável",
                yaxis_title="Quantidade",
            )

            # Gráfico de SSAs programadas por semana
            week_counts = (
                df_filtered.iloc[:, SSAColumns.SEMANA_PROGRAMADA]
                .value_counts()
                .sort_index()
            )
            fig_week = go.Figure(
                data=[go.Bar(x=week_counts.index, y=week_counts.values)]
            )
            fig_week.update_layout(
                title="SSAs Programadas por Semana",
                xaxis_title="Semana",
                yaxis_title="Quantidade",
            )

            # Detalhamento (visível apenas se houver filtro)
            detail_style = (
                {"display": "block"} if resp_prog or resp_exec else {"display": "none"}
            )

            # Gráficos de detalhamento
            state_counts = df_filtered.iloc[:, SSAColumns.SITUACAO].value_counts()
            fig_detail_state = go.Figure(
                data=[go.Bar(x=state_counts.index, y=state_counts.values)]
            )
            fig_detail_state.update_layout(
                title="SSAs Pendentes por Estado",
                xaxis_title="Estado",
                yaxis_title="Quantidade",
            )

            week_detail = (
                df_filtered.iloc[:, SSAColumns.SEMANA_PROGRAMADA]
                .value_counts()
                .sort_index()
            )
            fig_detail_week = go.Figure(
                data=[go.Bar(x=week_detail.index, y=week_detail.values)]
            )
            fig_detail_week.update_layout(
                title="SSAs Programadas por Semana (Detalhamento)",
                xaxis_title="Semana",
                yaxis_title="Quantidade",
            )

            # Dados da tabela filtrados
            table_data = self._prepare_table_data()
            if resp_prog:
                table_data = [
                    row for row in table_data if row["resp_prog"] == resp_prog
                ]
            if resp_exec:
                table_data = [
                    row for row in table_data if row["resp_exec"] == resp_exec
                ]

            return (
                fig_prog,
                fig_exec,
                fig_week,
                detail_style,
                fig_detail_state,
                fig_detail_week,
                table_data,
            )

    def run_server(self, debug=True, port=8050):
        """Inicia o servidor do dashboard."""
        self.app.run_server(debug=debug, port=port)

    def _get_initial_stats(self):
        """Calcula estatísticas iniciais para o dashboard."""
        try:
            total_ssas = len(self.df)

            # Contagem por prioridade
            prioridades = self.df.iloc[
                :, SSAColumns.GRAU_PRIORIDADE_EMISSAO
            ].value_counts()

            # SSAs críticas (S3.7)
            ssas_criticas = len(
                self.df[
                    self.df.iloc[:, SSAColumns.GRAU_PRIORIDADE_EMISSAO].str.upper()
                    == "S3.7"
                ]
            )

            # Contagem por setor
            setores = self.df.iloc[:, SSAColumns.SETOR_EXECUTOR].value_counts()

            # Contagem por estado
            estados = self.df.iloc[:, SSAColumns.SITUACAO].value_counts()

            # Análise temporal
            datas = pd.to_datetime(self.df.iloc[:, SSAColumns.EMITIDA_EM])
            data_mais_antiga = datas.min()
            data_mais_recente = datas.max()

            return {
                "total": total_ssas,
                "criticas": ssas_criticas,
                "taxa_criticidade": (
                    (ssas_criticas / total_ssas * 100) if total_ssas > 0 else 0
                ),
                "por_prioridade": prioridades,
                "por_setor": setores,
                "por_estado": estados,
                "periodo": {"inicio": data_mais_antiga, "fim": data_mais_recente},
                "responsaveis": {
                    "programacao": self.df.iloc[
                        :, SSAColumns.RESPONSAVEL_PROGRAMACAO
                    ].nunique(),
                    "execucao": self.df.iloc[
                        :, SSAColumns.RESPONSAVEL_EXECUCAO
                    ].nunique(),
                },
            }
        except Exception as e:
            logging.error(f"Erro ao calcular estatísticas iniciais: {str(e)}")
            # Retorna estatísticas vazias em caso de erro
            return {
                "total": 0,
                "criticas": 0,
                "taxa_criticidade": 0,
                "por_prioridade": pd.Series(),
                "por_setor": pd.Series(),
                "por_estado": pd.Series(),
                "periodo": {"inicio": None, "fim": None},
                "responsaveis": {"programacao": 0, "execucao": 0},
            }


class KPICalculator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_efficiency_metrics(self) -> Dict:
        """Calcula métricas de eficiência."""
        total_ssas = len(self.df) if len(self.df) > 0 else 1  # Prevent division by zero
        return {
            "taxa_programacao": len(
                self.df[self.df.iloc[:, SSAColumns.SEMANA_PROGRAMADA].notna()]
            )
            / total_ssas,
            "taxa_execucao_simples": len(
                self.df[self.df.iloc[:, SSAColumns.EXECUCAO_SIMPLES] == "Sim"]
            )
            / total_ssas,
            "distribuicao_prioridade": self.df.iloc[
                :, SSAColumns.GRAU_PRIORIDADE_EMISSAO
            ]
            .value_counts(normalize=True)
            .to_dict(),
        }

    def get_overall_health_score(self) -> float:
        """Calcula um score geral de saúde do sistema."""
        metrics = self.calculate_efficiency_metrics()
        score = (
            metrics["taxa_programacao"] * 0.5 + metrics["taxa_execucao_simples"] * 0.5
        )
        return round(score * 100, 2)

if __name__ == "__main__":
    try:
        # Test the dashboard with sample data
        import pandas as pd

        sample_df = pd.DataFrame()  # Create your sample DataFrame here
        dashboard = SSADashboard(sample_df)
        dashboard.run_server(debug=True, port=8050)
    except Exception as e:
        logging.error(f"Error starting dashboard: {str(e)}")
        raise
