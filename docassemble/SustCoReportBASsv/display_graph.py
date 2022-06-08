import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from docassemble.base.util import DAFile

# from PIL import Image

def sort_empty_df(obj):
  """function to populate none response with float 0.0 in the df for the graphs"""
  if len(obj) > 2:
    return float(obj)
  else:
    return float(0.0)

def show_graph_radar(
    t1, t2, t1_name, t2_name, categories, filename, visualization_image, height, width, color="#FFC000"
):

    visualization_image.initialize(filename=filename)

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            #r=[float(obj) for obj in t1.transpose()[0].to_list()],
            r=[sort_empty_df(obj) for obj in t1.transpose()[0].to_list()],
            theta=categories,
            fill="toself",
            name=t1_name,
            marker=dict(size=5, color=color),
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            #r=[float(obj) for obj in t2.transpose()[0].to_list()],  
            r=[sort_empty_df(obj) for obj in t2.transpose()[0].to_list()],
            theta=categories,
            fill="toself",
            name=t2_name,
            marker=dict(
                size=5,
                color="lightblue",
            ),
        )
    )
    # fig.add_trace(
    #    go.Scatterpolar(
    #        r=t3.transpose()[0].to_list(),
    #        theta=categories,
    #        # fill='toself',
    #        name="Betydelse för intressenter",
    #        marker=dict(
    #            size=5,
    #            color="red",
    #        ),
    #    )
    # )
    fig.update_layout(
        font_size=30,
        font_family="Menlo",
        font_color="#0270BF",
        polar=dict(radialaxis=dict(visible=True, range=[0, 1],tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1],)),## ticktext=["liten", "medel", "stor",])),
        showlegend=True,
        legend_font_size=28,
        width=width,
        height=height,
    )

    fig.write_image(visualization_image.path(), scale=2)
    plot = visualization_image
    return plot


def show_graph_scatter(df, filename, visualization_image, height, width):
    #! initiate a path to DAfile for image store - a unique file need to be store for each image.
    # scatter_back = Image.open("scatter_back.png")

    abbr = {
        "Verksamhetsstyrning": "A",
        "Mänskliga rättigheter": "B",
        "Arbetsförhållanden": "C",
        "Miljö": "D",
        "Goda verksamhetsmetoder": "E",
        "Konsumentfrågor": "F",
        "Samhällsengagemang och utveckling": "G",
    }

    df_group = pd.DataFrame(
        df.groupby(
            [
                "Verksamhetens nuvarande påverkan på ansvarsområdet",
                "Ansvarsområdets betydelse för verksamhetsmål",
            ]
        )
        .apply(lambda x: x["Ansvarsområde"].to_list())
        .reset_index()
    )
    df_group = df_group.rename(columns={0: "Ansvarsområde_List"})
    df_group["count"] = df_group["Ansvarsområde_List"].apply(lambda x: len(x))
    df_group["size"] = df_group["count"].apply(lambda x: np.log(x * 5))
    df_group["abbr_text"] = df_group["Ansvarsområde_List"].apply(
        lambda x: ", ".join([abbr[o] for o in x])
    )
    df_group["Ansvarsområde"] = df_group["Ansvarsområde_List"].apply(
        lambda x: "<br>".join(x)
    )

    visualization_image.initialize(filename=filename)

    fig = px.scatter(
        df_group,
        x="Verksamhetens nuvarande påverkan på ansvarsområdet",
        y="Ansvarsområdets betydelse för verksamhetsmål",
        size="size",
        size_max=15,
        labels="abbr_text",
        color="Ansvarsområde",
        symbol="Ansvarsområde",
        color_discrete_sequence=px.colors.qualitative.G10,
        # text="abbr_text", ##show the corresponding letters
    )
    fig.update_layout(
        # images=[
        #    dict(
        #        source=scatter_back,
        #        xref="paper",
        #        yref="paper",
        #        x=0,
        #        y=1,
        #        sizex=1,
        #        sizey=1,
        #        xanchor="left",
        #        yanchor="top",
        #        sizing="stretch",
        #        opacity=1,
        #        layer="below",
        #    )
        # ],
        font_family="Menlo",
        font_color="#0270BF",
        font_size=14,
        width=width,
        height=height,
        template="simple_white",
    )
    fig.update_traces(
        dict(marker_line_width=0.8, marker_line_color="black"),
        # textposition="top center"
    )
    fig.update_xaxes(range=[-0.1, 1.1], ticktext=["Negativ påverkan", "Positiv påverkan"],
    tickvals=[0.2, 0.8,],)
    fig.update_yaxes(range=[-0.1, 1.1], ticktext=["Låg betydelse", "Hög betydelse"],
    tickvals=[0.2, 0.8,],)
    
    fig.add_hline(
        y=0.5, line_width=1, line_dash="solid", line_color="blue", opacity=0.25
    )
    fig.add_vline(
        x=0.5, line_width=1, line_dash="solid", line_color="blue", opacity=0.25
    )

    fig.write_image(visualization_image.path(), scale=2)
    plot = visualization_image
    return plot


def create_df(table):
    #! Pandas cannot be pickled in DA so it need a python function to be established in a DA code block.
    """Input is a DA table that is converted to a pandas df. Note it need to be initated with the table varibles (eg. Thing)."""
    str(table)
    df = table.as_df()
    return df

  
  
  
def xlsx_transposed(table, filename, sheet_name):
    df = table.as_df().transpose()
    df.rename(columns={0:'data'}, inplace=True)
    outfile = DAFile()
    outfile.set_random_instance_name()
    outfile.initialize(filename=filename)
    writer = pd.ExcelWriter(outfile.path(),
                engine='xlsxwriter',
                options={'remove_timezone': True})
    df.to_excel(writer, sheet_name=sheet_name, index=True, freeze_panes=(1,0))
    writer.save()
    outfile.commit()
    outfile.retrieve()
    return outfile 
