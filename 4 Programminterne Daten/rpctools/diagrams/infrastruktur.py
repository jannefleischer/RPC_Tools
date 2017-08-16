# -*- coding: utf-8 -*-

import numpy as np
from rpctools.utils.diagram import MatplotDiagram
import matplotlib.ticker as mticker
from rpctools.utils.constants import Nutzungsart
from textwrap import wrap


class NetzlaengenDiagramm(MatplotDiagram):

    def _create(self, **kwargs):
        line_table = 'Erschliessungsnetze_Linienelemente'
        self.title = (u"{}: Länge der zusätzlichen Infrastrukturnetze "
                 u"(ohne punktuelle Maßnahmen)".format(
                     self.tbx.par.get_projectname()))
        x_label = u"Meter zusätzliche Netzlänge (ohne punktuelle Maßnahmen)"

        linien_df = self.tbx.table_to_dataframe(
            line_table, columns=['SHAPE_Length', 'IDNetz'],
            workspace='FGDB_Kosten.gdb'
        )
        base_df = self.tbx.table_to_dataframe(
            'Netze_und_Netzelemente', workspace='FGDB_Kosten_Tool.gdb',
            columns=['IDNetz', 'Netz'],
            is_base_table=True
        )
        base_df.drop_duplicates(inplace=True)
        joined = linien_df.merge(base_df, on='IDNetz', how='right')
        joined.fillna(0, inplace=True)
        grouped = joined.groupby(by='IDNetz')
        categories = []
        lengths = []
        for id_netz, grouped_df in grouped:
            categories.append(grouped_df['Netz'].values[0])
            lengths.append(grouped_df['SHAPE_Length'].sum())

        figure, ax = self.plt.subplots(figsize=(10, 5))
        ax.tick_params(axis='both', which='major', labelsize=9)
        y_pos = np.arange(len(categories))
        ax.barh(y_pos, lengths, height=0.3, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        ax.set_title(self.title)
        ax.set_xlabel(x_label)
        ax.xaxis.grid(True, which='major')
        box = ax.get_position()
        ax.set_position([box.x0 + box.width * 0.12, box.y0,
                         box.width * 0.88, box.height])

        return ax


class MassnahmenKostenDiagramm(MatplotDiagram):

    def _create(self, **kwargs):
        point_table = 'Erschliessungsnetze_Punktelemente'
        self.title = u"{}: Kosten der punktuellen Maßnahmen (nur erstmalige Herstellung)".format(
            self.tbx.par.get_projectname())
        x_label = u"Kosten der punktuellen Maßnahmen (nur erstmalige Herstellung)"

        point_df = self.tbx.table_to_dataframe(
            point_table, workspace='FGDB_Kosten.gdb')
        base_df = self.tbx.table_to_dataframe(
            'Netze_und_Netzelemente', workspace='FGDB_Kosten_Tool.gdb',
            columns=['IDNetz', 'Netz'],
            is_base_table=True
        )
        base_df.drop_duplicates(inplace=True)

        joined = point_df.merge(base_df, on='IDNetz', how='right')
        joined.fillna(0, inplace=True)
        grouped = joined.groupby(by='IDNetz')
        categories = []
        costs = []
        for id_netz, grouped_df in grouped:
            categories.append(grouped_df['Netz'].values[0])
            costs.append(grouped_df['Euro_EH'].sum())

        figure, ax = self.plt.subplots(figsize=(10, 5))
        y_pos = np.arange(len(categories))
        ax.barh(y_pos, costs, height=0.3, align='center')
        ax.tick_params(axis='both', which='major', labelsize=9)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        ax.set_title(self.title)
        ax.set_xlabel(x_label)
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter(u'%d €'))
        ax.xaxis.grid(True, which='major')
        box = ax.get_position()
        ax.set_position([box.x0 + box.width * 0.12, box.y0,
                         box.width * 0.88, box.height])

        return ax


class GesamtkostenDiagramm(MatplotDiagram):

    def _create(self, **kwargs):
        legend = [u'1 - Kosten der erstmaligen Herstellung',
                  u'2 - Kosten für Betrieb und Unterhaltung in der ersten 20 Jahren',
                  u'3 - Anteilige Kosten der Erneuerung (bezogen auf einen Zeitraum von 20 Jahren)']
        workspace = 'FGDB_Kosten.gdb'
        table = 'Gesamtkosten'
        self.title = u"{}: Gesamtkosten der infrastrukturellen Maßnahmen in den ersten 20 Jahren".format(
            self.tbx.par.get_projectname())
        x_label = u"Kosten für Netzerweiterungen und punktuelle Maßnahmen"

        df_costs = self.tbx.table_to_dataframe(
            table, workspace=workspace
        )

        u, u_idx = np.unique(df_costs['Netz'], return_index=True)
        categories = df_costs['Netz'][np.sort(u_idx)]

        pos_idx = np.arange(len(categories))

        bar_width = 0.2
        spacing = 1.15

        figure, ax = self.plt.subplots(figsize=(10, 6))
        self.plt.gca().invert_yaxis()
        grouped = df_costs.groupby(by='IDKostenphase')
        phase_names = []

        text_offset =  max(df_costs['Euro']) * 0.07
        for i, (phase_id, group) in enumerate(grouped):
            costs = group['Euro'].values
            patches = ax.barh(pos_idx + i * bar_width * spacing, costs,
                              height=bar_width, align='center')
            phase_names.append(legend[group['IDKostenphase'].values[0]-1])

            for index, patch in enumerate(patches):
                width = patch.get_width()
                ax.text(width + text_offset,
                        pos_idx[index] + i * bar_width * spacing,
                        '%d' % int(width) + u' €', ha='center', va='center')

        ax.tick_params(axis='both', which='major', labelsize=9)
        ax.set_yticks(pos_idx + bar_width*spacing)
        ax.set_yticklabels(categories)
        ax.set_title(self.title)
        ax.set_xlabel(x_label)
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter(u'%d €'))
        ax.xaxis.grid(True, which='major')
        xmin, xmax = ax.get_xlim()
        ax.set_xlim(left=None, right=xmax*1.1, emit=True, auto=False)


        #ax.legend(phase_names, loc='upper right')
        box = ax.get_position()

        ax.set_position([box.x0 + box.width * 0.12, box.y0 + box.height * 0.2,
                         box.width * 0.88, box.height * 0.8])

        # Put a legend to the right of the current axis
        ax.legend(phase_names, loc='center left', bbox_to_anchor=(0, -0.3))
        return ax


class KostentraegerDiagramm(MatplotDiagram):
    colors = ['#005CE6', '#002673', '#894444', '#73FFDF', '#FFFF00']
    def _create(self, **kwargs):
        workspace = 'FGDB_Kosten.gdb'
        table = 'Gesamtkosten_nach_Traeger'
        self.title = (u"{}: Aufteilung der Gesamtkosten "
                      u"auf die Kostenträger".format(
                          self.tbx.par.get_projectname()))
        x_label = u"Kosten für Netzerweiterungen und punktuelle Maßnahmen"

        df_shares = self.tbx.table_to_dataframe(
            table, workspace=workspace
        )

        df_shareholders = self.tbx.table_to_dataframe(
            'Kostentraeger', workspace='FGDB_Kosten_Tool.gdb',
            is_base_table=True
        )
        categories = df_shareholders['Kostentraeger']
        cols = df_shareholders['spalte']

        pos_idx = np.arange(len(categories))

        bar_width = 0.5

        figure, ax = self.plt.subplots(figsize=(12, 5))
        self.plt.gca().invert_yaxis()

        colors = self.colors  #self.plt.cm.Paired(np.linspace(0, 1, len(df_shares)))

        summed = np.zeros(len(cols))

        for j, (index, net_share) in enumerate(df_shares.iterrows()):
            data = []
            for i, col in enumerate(cols):
                data.append(net_share[col])
            patches = ax.barh(pos_idx, data, left=summed, height=bar_width, color=colors[j])
            summed += data

        # Anfang: Balken beschriften
        text_offset = max(summed) * 0.02
        for i, patch in enumerate(patches.get_children()):
            width = patch.get_x() + patch.get_width()
            y_pos = patch.get_y()
            print y_pos
            ax.text(width + text_offset, i, str(round(width, 0)) + u' €', color='black',ha='left', va='center')  #, bbox=dict(facecolor='white', edgecolor='white', boxstyle="round"))
        x_min, x_max = ax.get_xlim()
        ax.set_xlim(x_min, x_max * 1.2)
        # Ende: Balken beschriften

        ax.tick_params(axis='both', which='major', labelsize=9)
        ax.set_yticks(pos_idx)
        ax.set_yticklabels(categories)
        ax.set_title(self.title)
        ax.set_xlabel(x_label)
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter(u'%d €'))
        ax.xaxis.grid(True, which='major')

        box = ax.get_position()
        ax.set_position([box.x0 + box.width * 0.2, box.y0 + box.height * 0.25,
                         box.width * 0.8, box.height * 0.75])

        # Put the legend to the right of the current axis
        ax.legend(df_shares['Netz'], loc='center left', bbox_to_anchor=(0, -0.35))
        # didn't find a way to pass custom colors directly
        for color, handle in zip(colors, ax.get_legend().legendHandles):
            handle.set_color(color)
        return ax


class VegleichsDiagramm(MatplotDiagram):
    _column = None
    _type_of_use = Nutzungsart.UNDEFINIERT


    def _create(self, **kwargs):
        self.title = (u'Vergleich: Erschließungskosten pro {} '
                      u'(in den ersten 25 Jahren)'.format(self._unit))
        x_label = (u'Gesamtkosten der Erschließung pro {} '
                   u'(in den ersten 25 Jahren)'.format(self._unit))

        df_areas = self.tbx.table_to_dataframe(
            'Teilflaechen_Plangebiet',
            workspace='FGDB_Definition_Projekt.gdb',
            columns=[self._column],
            where='Nutzungsart={}'.format(self._type_of_use)
        )
        df_reference = self.tbx.table_to_dataframe(
            'Vergleichswerte',
            workspace='FGDB_Kosten_Tool.gdb',
            where='IDNutzungsart={}'.format(self._type_of_use),
            is_base_table=True
        )
        df_costs = self.tbx.table_to_dataframe(
            'Gesamtkosten',
            workspace='FGDB_Kosten.gdb'
        )

        # there is only one row for each type of use
        df_reference = df_reference.iloc[0]
        x = df_areas[self._column].sum()
        total_costs = df_costs['Euro'].sum()
        costs_per_x = int((total_costs / x) / 1000) * 1000
        reference = df_reference['Wert']

        categories = [
            u'Vergleichswert (Schätzung):\n{}'
            .format(df_reference['Beschreibung']),
            u'Projekt "{}" (alle Netze, \nKostenphasen und Kostenträger)'
            .format(self.tbx.par.get_projectname())
        ]
        categories = ['\n'.join(wrap(c, 40)) for c in categories]

        figure, ax = self.plt.subplots(figsize=(9, 4))
        y_pos = np.arange(len(categories))
        bar_width = 0.5
        ax.barh(y_pos, [reference, costs_per_x], height=bar_width,
                align='center')  #, color=[ '#99aaff', '#2c64ff'])
        # Anfang: Balken beschriften
        text_offset = max([reference, costs_per_x]) * 0.02
        ax.text(reference + text_offset, y_pos[0] - 0.02,
                str(int(round(reference, 0))) + u' €', color='black')
        ax.text(costs_per_x + text_offset, y_pos[1] - 0.02,
                str(int(round(costs_per_x, 0))) + u' €', color='black')
        x_min, x_max = ax.get_xlim()
        ax.set_xlim(x_min, x_max*1.1)
        # Ende: Balken beschriften
        ax.tick_params(axis='both', which='major', labelsize=9)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        ax.set_title(self.title)
        ax.set_xlabel(x_label)
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter(u'%d €'))
        ax.xaxis.grid(True, which='major')
        box = ax.get_position()
        ax.set_position([box.x0 + box.width * 0.2, box.y0,
                         box.width * 0.8, box.height])
        return ax


class VergleichWEDiagramm(VegleichsDiagramm):
    _column = 'WE_gesamt'
    _type_of_use = Nutzungsart.WOHNEN
    _unit = 'Wohneinheit'


class VergleichAPDiagramm(VegleichsDiagramm):
    _column = 'AP_gesamt'
    _type_of_use = Nutzungsart.GEWERBE
    _unit = 'Arbeitsplatz'


if __name__ == "__main__":
    #diagram = VergleichAPDiagramm()
    #diagram.create()
    #diagram.show()
    #diagram = VergleichWEDiagramm()
    #diagram.create()
    #diagram.show()
    diagram = KostentraegerDiagramm()
    diagram.create()
    diagram.show()
    #diagram = MassnahmenKostenDiagramm()
    #diagram.create()
    #diagram.show()
    #diagram = NetzlaengenDiagramm()
    #diagram.create()
    #diagram.show()
    #diagram = GesamtkostenDiagramm()
    #diagram.create()
    #diagram.show()
