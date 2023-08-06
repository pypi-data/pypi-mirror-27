
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class PYbleau(object):
    
    def __init__(self):
        
        pass
        
        
    
    def py_mv_summary_and_visualization(self,dataframe):
        
        '''Input pandas Dataframe ---> 
        Returns Number of Rows and Columns. This method 
        also displays missing values numerical and visually'''
        
        
        print('There are {} rows and {} columns in this dataframe.'.format(dataframe.shape[0],dataframe.shape[1]))
        print(' ')
          
        print('Checking for Missing Values')
        print('--------------------------- ')
        print(' ')
    
        print(dataframe.isnull().sum())
        print(' ')
        
        
        fig = plt.figure(figsize=(18,8))
        axes = fig.add_subplot()
        
        sns.heatmap(dataframe.isnull(),yticklabels=False,cbar=False,ax=axes)
        plt.title('Missing values by columns',fontsize=(22))
        plt.xlabel('Columns',fontsize=(18))
        plt.ylabel('')
        plt.tight_layout()
        
        
              
    def py_mv_dataframe(self,dataframe):
        
        '''Input pandas Dataframe --->  Returns Missing Value Data frame'''
        missing_value_list = []
    
        for missing_value in dataframe.isnull().sum():
            missing_value_list.append(missing_value)
        
        column_name_list = []
        
        for column_name in dataframe.columns:
            column_name_list.append(column_name)


        dataframe = pd.DataFrame({'Column_Names': column_name_list,
              'Missing_Values_Count': missing_value_list})
        
        
        return dataframe.style.bar()    
    
    def py_univariant_hist_plot(self,series,xlabel='x',ylabel='y',title='Histogram Plot',sns_color ='darkgrid'):
        sns.set_style(sns_color)
        plt.figure(figsize=(19,10))
        sns.distplot(series,hist_kws=dict(edgecolor="k", linewidth=2), kde=False,color='b' )
        plt.rcParams["patch.force_edgecolor"] = True
        plt.xlabel(xlabel,fontsize=(15))
        plt.xlim(series.min(),series.max())
        plt.ylabel(ylabel,fontsize=(15))
        plt.title(title,fontsize=(20))
        
    def py_correlation_plot(self,dataframe,title='Correlation Plot',cmap='plasma'):
        plt.figure(figsize=(19,10))
        sns.heatmap(dataframe.corr(),annot=True,cmap=cmap)
        plt.title(title,fontsize=(22))
        plt.tight_layout()