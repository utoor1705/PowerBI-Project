import pandas as pd 

class StatsCanadaDataCleaner:
    """ A class used to preprocess Stats Canada datasets for analysis.
    
    Attributes:
        dataset (DataFrame): A Stats Canada dataset.
    """
    def __init__(self, dataset):
        """ Initializes the StatcanadaDataCleaner class with a dataset.
        
        Args:
            dataset (DataFrame): A Stats Canada dataset.
        """
        self.dataset = dataset
          
    def preprocess_data(self, unemployed_only=True, classification_data=False):
        """ Preprocesses dataset(s) for analysis, performing data selection, cleaning and transformation.
        
        Returns:
            dataset (DataFrame): Preprocessed dataset.
        """
        
        # Rename selected columns for readability
        new_col_dict = {
        'SURVYEAR': 'Year',
        'SURVMNTH': 'Month',
        'LFSSTAT': 'Labour Force Status', 
        'PROV': 'Province',
        'AGE_12': 'Age Group',
        'SEX': 'Gender',
        'EDUC': 'Education Level', 
        'IMMIG': 'Immigration Status',
        'NOC_10': 'Occupation of Job',
        'DURJLESS': 'Duration of Joblessness (Months)', 
        'SCHOOLN': 'Current Student Status',
        }    
        self.dataset = self.dataset.rename(columns=new_col_dict)
        
        # Drop columns that are not needed
        self.dataset = self.dataset[list(new_col_dict.values())]
        
        # Rename column values for readability
        self.dataset['Month'] = self.dataset['Month'].map({
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        })
            
        self.dataset['Labour Force Status'] = self.dataset['Labour Force Status'].map({
            1: 'Employed',
            2: 'Employed',
            3: 'Unemployed',
            4: 'Not in Labour Force',
        })
        
        self.dataset['Province'] = self.dataset['Province'].map({
            10: 'Newfoundland and Labrador',
            11: 'Prince Edward Island',
            12: 'Nova Scotia',
            13: 'New Brunswick',
            24: 'Quebec',
            35: 'Ontario',
            46: 'Manitoba',
            47: 'Saskatchewan',
            48: 'Alberta',
            59: 'British Columbia'
        })
        
        self.dataset['Age Group'] = self.dataset['Age Group'].map({
            1: '20 and below',
            2: '20 to 40 years',
            3: '20 to 40 years',
            4: '20 to 40 years',
            5: '20 to 40 years',
            6: '40 and above',
            7: '40 and above',
            8: '40 and above',
            9: '40 and above',
            10: '40 and above',
            11: '40 and above',
            12: '40 and above'
        })
        
        self.dataset['Gender'] = self.dataset['Gender'].map({
            1: 'Male',
            2: 'Female'
        })
        
        self.dataset['Education Level'] = self.dataset['Education Level'].map({
            1: 'Some high school',
            2: 'High school graduate',
            3: 'Some postsecondary',
            4: 'Postsecondary certificate or diploma',
            5: "Bachelor's degree",
            6: "Above bachelor's degree"
        })
               
        self.dataset['Immigration Status'] = self.dataset['Immigration Status'].map({
        1: 'Immigrant',
        2: 'Immigrant',
        3: 'Non-immigrant'
        })
        
        self.dataset['Occupation of Job'] = self.dataset['Occupation of Job'].map({
            1: 'Management Occupations',
            2: 'Business & Finance Occupations',
            3: 'Applied Science & Engineering Occupations',
            4: 'Health Occupations',
            5: 'Social, Education and Government Service Occupations',
            6: 'Arts, Culture, Recreation and Sport Occupations',
            7: 'Sales and Service occupations',
            8: 'Trades and Transportation occupations',
            9: 'Natural Resources and Agriculture occupations',
            10: 'Manufacturing and Utilities occupations',
        })
        
        self.dataset['Current Student Status'] = self.dataset['Current Student Status'].map({
            1: 'Non-student',
            2: 'Student (Full-time)',
            3: 'Student (Part-time)'
        })
                
        # Convert Year and Month to singular Date column
        self.dataset['Year'] = self.dataset['Year'].astype(str)
        self.dataset['Month'] = self.dataset['Month'].astype(str)
        self.dataset['Date'] = self.dataset['Year'] + '-' + self.dataset['Month']
        self.dataset['Date'] = pd.to_datetime(self.dataset['Date'])
        
        # Drop Year and Month Columns
        self.dataset = self.dataset.drop(columns=['Year', 'Month'])
           
        # Only Non-Students
        self.dataset = self.dataset[self.dataset['Current Student Status'] == 'Non-student']
        self.dataset = self.dataset.drop(columns=['Current Student Status'])
        
        # Remove those in Labour Force Status with 'Not in Labour Force'
        self.dataset = self.dataset[self.dataset['Labour Force Status'] != 'Not in Labour Force']

        # If unemployed_only is True, only keep those in Labour Force Status 'Unemployed'
        if unemployed_only:
            self.dataset = self.dataset[self.dataset['Labour Force Status'] == 'Unemployed']
            self.dataset = self.dataset.drop(columns=['Labour Force Status'])
        
        if classification_data:
            self.dataset = self.dataset.drop(columns=['Duration of Joblessness (Months)'])
           
        # Clear rows with NaN values 
        self.dataset = self.dataset.dropna()
            
        # Move Date column to the front for better readability
        cols = self.dataset.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        self.dataset = self.dataset[cols]
        
        # Return dataset   
        return self.dataset
    

# Notes:
# 1. Only for year 2023
# 2. Keep options open for adding more functions
# 3. Keep options open for adding more columns/metrics