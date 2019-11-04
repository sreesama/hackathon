import matplotlib.pyplot as plt
import pandas as pd
import six
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('EDA.pdf');


#Adding styles to the table
#---------------------------
def addStyletoTable(mpl_table):
    edge_color='w'
    header_color='green'
    row_colors=['#f1f1f2', 'w']
    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < 0:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])

def treatnullsifAny(df):
    for cols in df.columns:
        df[df[cols].isnull()][cols].fillna(0,inplace=True)


def startProcess(dfo,target):
    df = processTitle(dfo,target)
    processBasicDetails(df)
    processColumnDetails(df)
    processStats(df)
    processGraphs(df)
    processCorrMatrix(df)
    processCorrHeatMap(df)
    processPairPlot(df)
    pp.close()



# *****************************************************************
# Start Processing
# Title Page
def processTitle(dfo,target):
    if target != '':
        df = dfo.drop(columns=[target])
    else:
        df=dfo
    plt.figure(figsize=(15, 5))
    plt.axis('off')
    Title = "*******************************" + "\n" \
        + "   Exploratory Data Analysis   " + "\n" \
        + "*******************************" + "\n";
    plt.text(0.5, 0.5, Title, ha='center', va='center', style='italic', fontsize=35,
         bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 10})
    pp.savefig()
    return df



#Shape & Duplicates of the dataset:
#----------------------------------
def processBasicDetails(df):
    print('---> basic details in progress')

    Header = "Size of the DataSet:" +"\n";
    fig, ax = plt.subplots(figsize=(15,5))
    fig.suptitle(Header,fontweight='bold')

    def get_duplicate_cols(df: pd.DataFrame) -> pd.Series:
        return pd.Series(df.columns).value_counts()[lambda x: x>1]

    dupcols = get_duplicate_cols(df)

    duplicate_columns = '';
    for i in range(0, len(dupcols)):
        duplicate_columns = duplicate_columns + dupcols[i] + "\n";

    if (duplicate_columns == ''):
        duplicate_columns = 'None'

    dups = df[df.duplicated()]

    lst=[]

    lstd=[]
    lstd.append("No of Rows ")
    lstd.append(str(df.shape[0]))
    lst.append(lstd)

    lstd=[]
    lstd.append("No of Columns ")
    lstd.append(str(df.shape[1]))
    lst.append(lstd)

    lstd=[]
    lstd.append("No of Duplicate Rows")
    lstd.append(dups.shape[0])
    lst.append(lstd)

    lstd=[]
    lstd.append("Duplicate Columns")
    lstd.append(duplicate_columns)
    lst.append(lstd)

    headerdf = pd.DataFrame(lst,columns=['Attribute','Value'])

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    mpl_table = ax.table(cellText=headerdf.values, colLabels=headerdf.columns, loc='center')

    addStyletoTable(mpl_table)

    pp.savefig()
    plt.close()

#Column Data types, Null Values presence, IQR
#============================================
def processColumnDetails(df):
    print('---> column details in progress')

    nullDF = pd.DataFrame(df.isnull().sum()).reset_index();
    nullDF.columns = ['column','cnt']
    naDF = pd.DataFrame(df.isna().sum()).reset_index();
    naDF.columns = ['column','cnt']
    nullDF[nullDF['column'] == 'Pregnancies'].count

    lst=[]
    for col in df.columns:
        if (df[col].dtype.name != 'object' and  (df[col].dtype.name != 'category') ):
            lstd=[]
            lstd.append(col)
            lstd.append(str(df[col].dtype))
            Q3 = df[col].quantile(.75).round(3)
            Q1 = df[col].quantile(.25).round(3)
            lstd.append(Q3 - Q1)

            if(df[df[col] > Q3 + 1.5 * (Q3-Q1)][col].count() != 0 or df[df[col] < Q1 - 1.5 * (Q3-Q1)][col].count()):
                lstd.append("Outliers Present")
            else:
                lstd.append("No Outliers")
            a = nullDF[nullDF['column'] == col]['cnt'].values
            b = naDF[naDF['column'] == col]['cnt'].values
            if (a > 0 | b > 0):
                lstd.append('Has Null')
            else :
                lstd.append('No Null')
            if (df[col].dtype.name != 'datetime64[ns]'):
                lstd.append(df[col].median().round(3))
                lstd.append(df[col].mode().values[0].round(3))
            lst.append(lstd)

    colddf = pd.DataFrame(lst,columns=['Column Name','Data Type', 'IQR','Outliers','Has Null', 'Median', 'Mode'])


    fig, ax = plt.subplots(figsize=(15,5))
    fig.suptitle("COLUMN DETAILS",fontweight='bold')

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    mpl_table = ax.table(cellText=colddf.values, colLabels=colddf.columns, loc='center')

    addStyletoTable(mpl_table)

    pp.savefig()
    plt.close()

#Basic Stats of the Data
#=========================
def processStats(df):
    print('---> stats in progress')

    fig, ax = plt.subplots(figsize=(15,5))
    fig.suptitle("DATASET STATISTICS",fontweight='bold')

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    statsdf = df.describe().round(3).transpose()
    statsdf.reset_index(inplace=True)
    statsdf.rename(columns={'index':'Column'},inplace=True)
    mpl_table = ax.table(cellText=statsdf.values, colLabels=statsdf.columns, loc='center')

    mpl_table.auto_set_font_size(True)
    mpl_table.set_fontsize(10)


    addStyletoTable(mpl_table)

    pp.savefig()
    plt.close()

#Skew, Kurt and other stats of the Data.
#======================================
def processAdditionalStats(df):

    print('---> additional stats in progress')

    lst=[]
    for cols in df.columns:
        if (df[cols].dtype.name != 'object' and  (df[cols].dtype.name != 'category') ):
            lstd=[]
            lstd.append(cols)
            lstd.append(df[cols].skew())
            lstd.append(df[cols].kurt())
            lstd.append(df[cols].min())
            lstd.append(df[cols].max())
            lst.append(lstd)

    sk = pd.DataFrame(lst,columns=['Column','Skew', 'Kurt','Minimum', 'Maximum'])

    fig, ax = plt.subplots(figsize=(15,5))
    fig.suptitle("ADDITIONAL STATISTICS",fontweight='bold')

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')


    mpl_table = ax.table(cellText=sk.values, colLabels=sk.columns, loc='center')

    addStyletoTable(mpl_table)


    pp.savefig()
    plt.close()

#=========================
def processGraphs(df):

    print('---> graphs in progress')

    treatnullsifAny(df)
    for cols in df.columns:
        if (df[cols].dtype.name == 'object'  or (df[cols].dtype.name == 'category') ):
            fig, axes = plt.subplots(figsize=(15,5))
            fig.suptitle("COUNT PLOT FOR "+ str(cols).upper(),fontweight='bold')
            sns.countplot(x=cols, data=df)
        else:
            if (df[cols].dtype.name != 'datetime64[ns]'):
                fig, axes = plt.subplots(nrows=1, ncols=3,figsize=(15,5))
                fig.suptitle("VARIOUS PLOTS FOR "+ str(cols).upper(),fontweight='bold')
                sns.distplot(df[cols],ax=axes[2])
                sns.boxplot(data=df[cols], ax=axes[0],color='green')
                sns.violinplot(data=df[cols], ax=axes[1])
                axes[0].set(ylabel=cols)
                axes[1].set(ylabel=cols)
                axes[2].set(xlabel=cols)
        pp.savefig()
        plt.close()

#Coorelation Matric
#=========================
def processCorrMatrix(df):

    print('---> corr matrix in progress')

    fig, ax = plt.subplots(figsize=(15,5))
    fig.suptitle("COORELATION MATRIX",fontweight='bold')

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    corrDF = df.corr().round(3)
    #corrDF.rename(columns={'index':'Column'}, inplace=True)


    mpl_table = ax.table(cellText=corrDF.values, colLabels=corrDF.columns, loc='center')

    addStyletoTable(mpl_table)

    pp.savefig()
    plt.close()


#Coorelation HeatMap
#=========================
def processCorrHeatMap(df):

    print('---> heatmap in progress')

    fig, axes = plt.subplots(figsize=(15,15))
    fig.suptitle("CORRELATION HEATMAP",fontweight='bold')

    sns.heatmap(df.corr())
    pp.savefig();

#Pairplot
#=========================
def processPairPlot(df):

    print('---> pairplot in progress')
    fig, axes = plt.subplots(figsize=(15,15))
    fig.suptitle("PAIRPLOT",fontweight='bold')

    sns.pairplot(df)
    pp.savefig();

