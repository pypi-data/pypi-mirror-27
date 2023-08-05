# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2017
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------

from pixiedust.display.chart.renderers import PixiedustRenderer
from pixiedust.display.chart.colorManager import Colors
from .bokehBaseDisplay import BokehBaseDisplay
from pixiedust.utils import Logger
from bokeh.plotting import figure
import pandas as pd
import numpy as np
import sys

try:
    from bkcharts import Line
except ImportError:
    from bokeh.charts import Line

@PixiedustRenderer(id="lineChart")
@Logger()
class LineChartRenderer(BokehBaseDisplay):
    def isSubplot(self):
        return self.options.get("lineChartType", "grouped") == "subplots"

    def getExtraFields(self):
        if not self.isSubplot() and len(self.getValueFields())>1:
            #no clusterby if we are grouped and multiValueFields
            return []
    
        clusterby = self.options.get("clusterby")
        return [clusterby] if clusterby is not None else []

    def safeList(self, index):
        if np.issubdtype(index.dtype, np.datetime64):
            dateFormat = self.options.get("dateFormat", None)
            def convert(x):
                return str(x).replace(':','-') if dateFormat is None else x.strftime(dateFormat)
            return [convert(pd.to_datetime(x)) for x in index.values]
        return index.values.tolist()

    def createBokehChart(self):
        keyFields = self.getKeyFields()
        valueFields = self.getValueFields()
        clusterby = self.options.get("clusterby")
        subplots = self.isSubplot()
        workingPDF = self.getWorkingPandasDataFrame().copy()

        for index, row in workingPDF.iterrows():
            for k in keyFields:
                if isinstance(row[k], str if sys.version >= '3' else basestring):
                    row[k] = row[k].replace(':', '.')
            workingPDF.loc[index] = row

        charts=[]
        if clusterby is not None and (subplots or len(valueFields)<=1):
            subplots = subplots if len(valueFields)==1 or subplots else False
            for j, valueField in enumerate(valueFields):
                pivot = workingPDF.pivot(
                    index=keyFields[0], columns=clusterby, values=valueField
                )

                if not subplots:
                    fig = figure(x_range=self.safeList(pivot.index) if not np.issubdtype(pivot.index.dtype, np.number) else None)
                    charts.append(fig)
                for i,col in enumerate(pivot.columns[:10]): #max 10
                    if subplots:
                        charts.append( 
                            Line(
                                pivot[col].values, color=Colors.hexRGB( 1.*i/2 ), ylabel=valueField, xlabel=keyFields[0], legend=False, 
                                title="{0} = {1}".format(clusterby, pivot.columns[i])
                            )
                        )
                    else:
                        xValues = pivot.index.values.tolist()
                        if not np.issubdtype(pivot.index.dtype, np.number):
                            xValues = range(1, len(xValues)+1)
                        fig.line(x = xValues, y = pivot[col].values, color = Colors.hexRGB( 1.*i/2 ), legend=str(col) if self.showLegend() else None)
        else:
            if subplots:
                for i,valueField in enumerate(valueFields):
                    charts.append(Line(workingPDF, x = keyFields[0], y=valueField, color = Colors.hexRGB( 1.*i/2 ), legend=self.showLegend(), plot_width=int(800/len(valueFields))))
            else:
                charts.append(Line(workingPDF, x = keyFields[0], y=valueFields, color=valueFields, legend=self.showLegend()))

            if clusterby is not None:
                self.addMessage("Warning: 'Cluster By' ignored when grouped option with multiple Value Fields is selected")
        return charts