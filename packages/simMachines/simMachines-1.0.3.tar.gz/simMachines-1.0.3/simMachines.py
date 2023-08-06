import requests
import base64
import json
import numpy as np
from getpass import getpass
import os
import pandas as pd

"""
Updates:
    - All API calls status codes verified before any other action
    - If data not uploaded to GUI, user does not have to input header parameters 
    outside of the data variables. 
    - Input data format supports pandas data frame or series, as well as numpy arrays
"""

class Authenticate():
    def __init__(self,*, username = '', password = '', path = '127.0.0.1',port = '9090',https = False):
        credentials = {}
        self.credentials = credentials 
        self.path = path
        self.port = port
        self.https = https
        self.credentials['path'] = self.path
        self.credentials['port'] = self.port
        self.credentials['https'] = self.https
        if username:
            self.username = username 
        else:
            username = input("Enter username: ")
            self.username = username
        self.credentials['username'] = self.username
        if password:
            self.password = password 
        else:
            password = getpass("Enter password: ")
            self.password = password             

        b64password = base64.b64encode(password.encode())
        self.b64password = b64password.decode()  
        self.credentials['b64password'] = self.b64password        
        ## Verifying username and password
        verify_URL = 'https' + '://' + self.path + ':' + self.port + '/cloud/verifyUser' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud/verifyUser'
        resp_verify = requests.get(verify_URL,auth=(self.username, self.b64password))
        if resp_verify.status_code == 200:
            authform = username + ':' + password
            filepassword = base64.b64encode(authform.encode())
            filepassword = filepassword.decode()
            filepassword = 'Basic ' + filepassword        
            self.filepassword = filepassword
            self.credentials['filepassword'] = self.filepassword
            print(resp_verify.content.decode())
        else:
            raise AttributeError(resp_verify.content.decode())

class Leliel():
    def __init__(self,**authenticate_creds):
        self.filepassword = authenticate_creds['filepassword']
        self.username = authenticate_creds['username']
        self.b64password = authenticate_creds['b64password']
        self.https = authenticate_creds['https']
        self.path = authenticate_creds['path']
        self.port = authenticate_creds['port']

        
        ## Second verification of username and password
        verify_URL = 'https' + '://' + self.path + ':' + self.port + '/cloud/verifyUser' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud/verifyUser'
        resp_verify = requests.get(verify_URL,auth=(self.username, self.b64password))
        if resp_verify.status_code != 200:
            raise AttributeError("Username-Password combination not recognized. Please try again.")

    def fit(self, *, X='', y='', DataUploaded = True, FileName = '', specs={},
            instanceName = '',folderName = '', specFileName = '',verbose=True, Pivots = 256,
            Probability = .95, AcceptedError = 1.2, Bins = 10, K = 10,
            TopColumns = 20, Length = 2, DenseMode = 'SMART', EnergyWeight = True,
            Threshold = .5, ClassificationK = -1, Storage = 1, Parallelism = 2,
            PivotSampleSize = 20000, CacheSize = 1000000, IndexCount = 3, MaximumBytesPerObject = 500000,
            IndexSampleSize = 100):
        """
        Train a Leliel instance
        
        Parameters
        ----------
        X: array or pandas DataFrame (default = ''), shape = (n_samples, n_features). Training data. If X is an array, the first row must be the headers. If X is a pandas DataFrame, the column names will be used as the headers. Optional, only needed if 'DataUploaded' is set to False.\n 
        y: array, pandas Series. (default =''), shape = (n_samples,). Target values. If y is an array, the first value must be the header. If y is a pandas Series, the name of the Series will be used as the header. Optional, only needed if 'DataUploaded' is set to False.\n
        DataUploaded: boolean (default = True). If training data already uploaded to simMachines's software, set to True. If not, set to False and angels can be trained on new data not yet uploaded to the software by passing variables X and y to the classifier. 
        FileName: string (default = ''). Name of the data file if new data is being used to train classifier. Optional, not needed if DataUploaded = True. 
        specs: dictionary (default = {}). Data specification types for training data. Dictionary keys represent the header names, and the values represent the data types. Optional, highly recommended if DataUploaded = False. 
        instanceName: string (default = ''), Name of instance to be trained.\n
        folderName: string (default = ''), Name of folder containing training data.\n
        specFileName: string (default = ''), Name of spec file to use for training. If empty, the most recent compatible file will be chosen.\n
        verbose: bool (default = True). Enable verbose output\n
        Pivots: int (default = 256), The number of primary search points in the engine. This may improve query speed at the cost of training time. (Range 256 to 1024)\n
        Probability: float (default = .95), Minimum accepted probability that the distance between the result and the query will be within the Accepted Error range.  Any result with lower probability will be discarded.\n
        AcceptedError: float (default = 1.2), Maximum accepted difference in distance between returned objects and the query object (Minimum = 1).\n
        Bins: int (default = 10), Specifies the number of ranges to be used in calculating the similarity of REAL columns.\n
        K: int (default = 10), Specify the k number of results for the nearest neighbor search.\n
        TopColumns: int (default = 20), The number of columns to consider for each prediction. Note that columns with strings, such as Multi_English, can be divided into multiple columns for this purpose.\n
        Length: int (default = 2), The total number of classes to consider for each prediction.\n
        DenseMode: string (default = 'SMART'), Sets the distance function used. Impacts weighting of factors (Also accepts: DEFAULT, MARQ3, EXCEEDS).\n
        EnergyWeight: bool (default = True), Useful if one classification is expected to be a significantly larger proportion of the results.\n
        Threshold: float (default = .5), The confidence level above which a class is considered an acceptable prediction. Non-default values are useful for unbalanced class distributions.\n
        ClassificationK: int (default = -1), Classifier K, the number of nearest neighbors used in making the classification (Default CK = Auto Detect).\n
        Storage: int (default = 1)\n
        Parallelism: int (default = 2)\n
        PivotSampleSize: int (default = 20000)\n
        CacheSize: int (default = 1000000)\n
        IndexCount: int (default = 3)\n
        MaximumBytesPerObject: int (default = 500000)\n
        IndexSampleSize: int (default = 100)
        """
        
        ## Building base URL's
        base_cloud_url = 'https' + '://' + self.path + ':' + self.port + '/cloud' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud'
        self.base_cloud_url = base_cloud_url
        base_v2_url = 'https' + '://' + self.path + ':' + self.port + '/V2.0' if self.https else 'http' + '://' + self.path + ':' + self.port + '/V2.0'
        self.base_v2_url = base_v2_url
        
        ## Checking if folderName exists
        if folderName:
            if instanceName:
                self.instanceName = instanceName
                if DataUploaded:
                    ## Warnings
                    if X:
                        raise Warning("Since 'DataUploaded' = True, 'X' will be ignored.")
                    if y:
                        raise Warning("Since 'Datauploaded' = True, 'y' will be ignored.")
                    if FileName:
                        raise Warning("Since 'DataUploaded' = True, 'FileName' will be ignored.")
                    
                    ## Getting Specs from folder
                    specs_URL = self.base_cloud_url +'/listSpecByFolder?folderName=' + folderName
                    resp_specs = requests.get(specs_URL,auth=(self.username, self.b64password))
                    if resp_specs.status_code == 200:
                        specs_json = json.loads(resp_specs.content.decode())
                        columns_str = 'COLUMNS='
                        valid_specFileName = 0
                        createdDate = 0
                        for spec_file in specs_json['list']:
                            if 'LELIEL' in spec_file['angelName']:
                                if specFileName:
                                    if specFileName == spec_file['fileName']:
                                        valid_specFileName = 1
                                        for col in spec_file['specsMap'].keys():
                                            columnName = col
                                            specType = spec_file['specsMap'][col]
                                            columns_str += columnName + ':' + specType + ','
                                else:
                                    ## If specFileName not given by user, choose most 
                                    ## recent compatible file present 
                                    createdDate_curr = spec_file['createdDate']
                                    if createdDate_curr > createdDate:
                                        createdDate = createdDate_curr
                                        for col in spec_file['specsMap'].keys():
                                            columnName = col
                                            specType = spec_file['specsMap'][col]
                                            columns_str += columnName + ':' + specType + ','
                    else:
                        raise AttributeError(resp_specs.content.decode())
                    
                    ## Error message if specFileName not recognized
                    if not valid_specFileName and specFileName:
                        raise AttributeError('Spec file name not recognized. Make sure to include file extension (.json, .tsv, etc.) in specFileName variable')
                
                ## New data not uploaded yet is being used to train angel
                else:                  
                    ## Warnings
                    if not specs:
                        raise Warning("Data type specifications ('specs') not provided. Automated specification types will be used in model creation. However, it is recommended that spec files are created by the user to improve model performence.")
                    
                    if specFileName:
                        raise Warning("A spec file name was provided for data not yet uploaded to aimMachines's software. 'specFileName' will be ignored.")
                        
                    if isinstance(X,pd.DataFrame):
                        HeadersX = list(X.columns)
                        X = np.asarray(X)
                    elif isinstance(X,pd.Series):
                        HeadersX = [X.name]
                        X = np.asarray(X)
                    else:
                        if len(X) > 0:
                            HeadersX = list(X[0])
                            X = np.asarray(X)
                        else:
                            raise AttributeError('X must be provided if DataUploaded == False')
                            
                    if isinstance(y,pd.DataFrame):
                        HeaderY = list(y.columns)[0]
                        y = np.asarray(y)
                    elif isinstance(y,pd.Series):
                        HeaderY = y.name
                        y = np.asarray(y)
                    else:
                        if len(y) > 0:
                            HeaderY = list(y[0])
                            y = np.asarray(y)
                        else:
                            raise AttributeError('y must be provided if DataUploaded == False')        
                        
                    if not FileName:
                        raise AttributeError('Missing file name (FileName) for data to be uploaded.')

                    ## Create folder if "folderName" is not already created
                    listFolders_URL = self.base_cloud_url +'/listFolders'
                    resp_folders = requests.get(listFolders_URL,auth=(self.username, self.b64password))
                    if resp_folders.status_code == 200:
                        resp_folders_json = json.loads(resp_folders.content.decode())
                        folder_exists = 0
                        for item in resp_folders_json['list']:
                            if item['name'] == folderName:
                                folder_exists = 1
                    else:
                        raise AttributeError(resp_folders.content.decode())
                            
                    if not folder_exists:
                        createFolder_URL = self.base_cloud_url +'/createFolder'
                        folder_data = {"folderName" : folderName}
                        resp_CreateFolder = requests.post(createFolder_URL,data = folder_data,auth=(self.username, self.b64password))
                        if resp_CreateFolder.status_code == 200:
                            pass
                        else:
                            raise AttributeError(resp_CreateFolder.content.decode())
                    else:
                        raise AttributeError('Folder with name %s already exists.' % folderName)
                        
                    ## Upload data to "folderName"
                    uploadFile_URL = self.base_cloud_url + '/uploadFile'
                    ## Validating shape of input data
                    if X.shape[0] != y.shape[0]:
                        raise ValueError('X and y have incompatible shapes.')
                        
                    if X.shape[1] != len(HeadersX):
                        raise ValueError('X.shape[1] must equal the length of HeadersX')

                        
                    with open(FileName,'wb') as r:
                        ## Header
                        header_string = '\t'.join(HeadersX) + '\t' + str(HeaderY) + '\n'
                        r.write(header_string.encode('utf8'))
                        for i,row in enumerate(X):
                            row_str = '\t'.join([str(val) for val in row.tolist()]) + '\t' +str(y[i])
                            if i == (len(X)-1):
                                pass
                            else:
                                row_str += '\n'
                            r.write(row_str.encode('utf8'))
                        r.flush()
                    r.close()
                    
                    filesize = os.path.getsize(FileName)
                    
                    with open(FileName,'rb') as f:
                        file_stream = {'fileData' : f}
                        file_data = {'fileName' : FileName
                                  ,'fileSize' : filesize
                                  ,'folderName' : folderName
                                  ,'authorization' : self.filepassword
                                  }
                        resp_file = requests.post(uploadFile_URL
                                             ,files = file_stream
                                                  ,data = file_data
                                                  ,auth = (self.username, base64.b64decode(self.b64password).decode()))
                    f.close()
                    os.remove(FileName)
                    
                    ## Raise error if file upload API call not successfull
                    if resp_file.status_code == 200:
                        pass
                    else:
                        raise AttributeError(resp_file.content.decode())
                    
                    ## Create spec file
                    columns_str = 'COLUMNS='
                    if not specs:
                        # Use recommended specs from /getSpecsOfFolder
                        getSpecs_URL = self.base_cloud_url + '/getSpecsOfFolder?folderName=' + folderName
                        resp_specs = requests.get(getSpecs_URL,auth=(self.username,self.b64password))
                        if resp_specs.status_code == 200:
                            resp_specs_json = json.loads(resp_specs.content.decode())
                            for item in resp_specs_json['columns']:
                                col_name = item['columnName']
                                if col_name == HeaderY:
                                    spec_type = 'CLASS'
                                else:
                                    spec_type = item['typeOfColumn']
                                columns_str += col_name + ':' + spec_type + ','
                        else:
                            raise AttributeError(resp_specs.content.decode())
                    else:
                        for item in specs.items():
                            col_name, spec_type = item
                            if col_name == HeaderY:
                                spec_type = 'CLASS'
                            columns_str += col_name + ':' + spec_type + ','                    
                    
                    
                ## If number of neighbors specified, hardcode in the API string
                if ClassificationK == -1:
                    fixedK = '_@_@_FIXED_K=false'
                else:
                    fixedK = '_@_@_FIXED_K=true'
                
                ## Converting boolean into string
                energy_weight_str = 'true' if EnergyWeight else 'false'
                
                columns_str = columns_str[:-1]
                params_str = columns_str + '_@_@_K=' + str(K) + '_@_@_PIVOTS=' + str(Pivots) + '_@_@_PROBABILITY=' + str(Probability) + \
                            '_@_@_ACCEPTED_ERROR=' + str(AcceptedError) + '_@_@_TOP_COLUMNS=' + str(TopColumns) + '_@_@_DENSE_MODE=' + DenseMode + \
                            '_@_@_ENERGY_WEIGHT=' + energy_weight_str + '_@_@_THRESHOLD=' + str(Threshold) + '_@_@_BINS=' + str(Bins) + '_@_@_LENGTH=' + \
                            str(Length) + fixedK +'_@_@_CLASSIFICATION_K='  + str(ClassificationK) + '_@_@_EXECUTE_FOLD=false' + '_@_@_PIVOT_SAMPLE_SIZE=' + \
                            str(PivotSampleSize) + '_@_@_CACHE_SIZE=' + str(CacheSize) + '_@_@_INDEX_COUNT=' + str(IndexCount) + '_@_@_MAXIMUM_BYTES_PER_OBJECT=' + \
                            str(MaximumBytesPerObject) + '_@_@_INDEX_SAMPLE_SIZE=' + str(IndexSampleSize)
                ## Building API call
                instance_data = {"instanceName" : instanceName,
                                 "folderName" : folderName,
                                 "angelName": 'LELIEL',
                                 "params": params_str,
                                 "storage" : Storage,
                                 "parallelism" : Parallelism,
                                 "authorization" : self.filepassword
                        }
                ## POST request to create instance
                createInstance_url = self.base_cloud_url + '/createInstance'
                resp = requests.post(createInstance_url,data = instance_data, auth = (self.username, self.b64password))
                
                if resp.status_code == 200:
                    listInstances_url = self.base_cloud_url + '/listInstances'
                    status = 'Unknown'
                    while status not in ('RUNNNING', 'BUILD_ERROR'):
                        resp_status = requests.get(listInstances_url, auth=(self.username, self.b64password))
                        if resp_status.status_code == 200:
                            resp_JSON = json.loads(resp_status.content.decode())
                        
                            ## looping through instances
                            for l in resp_JSON['list']:
                                if l['label'] == self.instanceName:
                                    status_curr = l['status']
                                    if status != status_curr:
                                        status = status_curr
                                        if verbose:
                                            print('Status: ' + status)
                                        else:
                                            pass
                        else:
                            raise AttributeError(resp_status.content.decode())
                            
                        if status == 'RUNNING':
                            print("Instance '" + self.instanceName + "' is ready for querying.")
                            break
                        elif status == 'BUILD_ERROR':
                            print("Instance '" + self.instanceName + "' returned a status of '" + status + "'.")
                            break
                        
                else:
                    ## If instance not created, set instance name to '' 
                    self.instanceName = ''
                    raise AttributeError(resp.content.decode())
            else:
                raise AttributeError("Must enter instance name as 'instanceName' variable")
        else:
            raise AttributeError("Must specify name of folder to train Leliel with (folderName variable).")
        
        return self
    
        
    def predict(self, X,*,version = ''):
        """
        Predict using trained Leliel instance, returns class.
        
        Parameters
        ----------
        X: {array-like}. Samples to predict. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        y_pred: array, shape = (n_samples,)
        Class labels for samples in X
        """
        
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            y_pred=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    sample_str = '\t'.join(samp)
                    queryObject_url = self.base_cloud_url + '/queryObject'
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryObject_url,data = query_data, auth = (self.username, self.b64password))
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        winning_class = resp_query_json['winnerUsingThreshold']['predictedClass']
                        y_pred.append(winning_class)
                    else:
                        failed_queries+=1
                        error_message = resp_query.content.decode()
                        
                if not failed_queries:
                    return np.asarray(y_pred)
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")
                
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")
            
        
    def predict_confidence(self, X,*,version = ''):
        """
        Predict using trained Leliel instance, returns confidence score. 
        
        Parameters
        ----------
        X: {array-like}. Samples to predict. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        y_pred: array, shape = (n_samples,)
        Prediction confidences for samples in X
        """
        
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            y_pred=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    sample_str = '\t'.join(samp)
                    queryObject_url = self.base_cloud_url + '/queryObject'
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryObject_url,data = query_data, auth = (self.username, self.b64password))
                    
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        winning_score={}
                        for result in resp_query_json['results']:
                            winning_score[result['predictedClass']] = result['score']
                        y_pred.append(winning_score)
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                if not failed_queries:
                    return np.asarray(y_pred)
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")
                
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")

    def get_neighbors(self, X, *,version = ''):
        """
        Retrive neighbors using trained Leliel instance.
        
        Parameters
        ----------
        X: {array-like}. Samples to retrieve neighbors for. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        neighbors_final: list of dictionaries, shape = (n_samples,(Classification K * Length,2))
        ID, distance pairs of nearest neighbors
        """
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            neighbors_final=[]
            if samples.shape[0]> 0:
                failed_queries=0
                for samp in samples:
                    sample_str = '\t'.join(samp)
                    queryObject_url = self.base_cloud_url + '/queryVisualization'            
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryObject_url,data = query_data, auth = (self.username, self.b64password))
                    
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        
                        ## Extracting neighbors for each class, sorting by distance 
                        ## in ascending order regardless of class
                        neighbors_dict={}
                        for class_ in resp_query_json['listMap'].keys():
                            distance_l=[]
                            id_l=[]
                            for neighbor in resp_query_json['listMap'][class_]['queryRelatedObject']:
                                distance = neighbor['distance']
                                objectId = neighbor['objectId']
                                distance_l.append(distance)
                                id_l.append(objectId)
                            neighbors = [(id_0,float(dist)) for dist,id_0 in sorted(zip(distance_l,id_l),reverse=False)]
                            neighbors_dict[class_] = neighbors
                        neighbors_final.append(neighbors_dict)
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                        
                if not failed_queries:
                    return neighbors_final
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")           
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")
            
    def get_factors(self, X, *, version = ''):
        """
        Returns local "Why" factors for each prediction.
        
        Parameters
        ----------
        X: {array-like}. Samples to predict. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        y_factors: array, shape = (n_samples,(n_features,3)
        Feature/value pairs, predictive weights, and boolean variable depicting if 
        feature/value pair is similar to the query object or not. This is 
        provided for each sample prediction in X.
        """
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            y_factors=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    sample_str = '\t'.join(samp)
                    queryVisualization_url = self.base_cloud_url + '/queryVisualization'            
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryVisualization_url,data = query_data, auth = (self.username, self.b64password))
                               
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        predicted_class = resp_query_json['rawQueryResponse']['winnerUsingThreshold']['predictedClass']
                        
                        ## Loop through query response, extract feature value pairs 
                        ## along with their local weights for predicted class
                        feature_value_pairs=[]
                        weights=[]
                        similar_to_query=[]
                        for item in resp_query_json['listMap'][predicted_class]['globalQueryObjects']:
                            feature_value_pairs.append(item['matchedItem'])
                            weights.append(float(item['weight']))
                            similar_to_query.append(item['similarToQuery'])
                        y_factors.append(list(zip(feature_value_pairs,weights,similar_to_query)))
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                        
                if not failed_queries:
                    return y_factors
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")           
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")                    
       
            
class LelielAljunied():
    def __init__(self, **authenticate_creds):
        self.filepassword = authenticate_creds['filepassword']
        self.username = authenticate_creds['username']
        self.b64password = authenticate_creds['b64password']
        self.https = authenticate_creds['https']
        self.path = authenticate_creds['path']
        self.port = authenticate_creds['port']

        ## Second verification of username and password
        verify_URL = 'https' + '://' + self.path + ':' + self.port + '/cloud/verifyUser' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud/verifyUser'
        resp_verify = requests.get(verify_URL,auth=(self.username, self.b64password))
        if resp_verify.status_code != 200:
            raise AttributeError("Username-Password combination not recognized. Please try again.")

    def fit(self,*, X='', y='', DataUploaded = True,FileName = '', specs={},
            instanceName = '',folderName = '', specFileName = '',verbose=True, Pivots = 256,
            Probability = .95, AcceptedError = 1.2, Bins = 10, K = 10,
            TopColumns = 20, Length = 2, DenseMode = 'SMART', EnergyWeight = 'true',
            Threshold = .5, ClassificationK = -1, Storage = 1, Parallelism = 2,
            PivotSampleSize = 20000, CacheSize = 1000000, IndexCount = 3, MaximumBytesPerObject = 500000,
            IndexSampleSize = 100, Seed = 563131, Iterations = 1000, LearningRate = 0.1, 
            FeatureSubsampling = 1.0, FeatureFocus = 10, ClassWeighting = 'UNIFORM'):

        """
        Train a Leliel Aljunied instance
        
        Parameters
        ----------
        X: array or pandas DataFrame (default = ''), shape = (n_samples, n_features). Training data. If X is an array, the first row must be the headers. If X is a pandas DataFrame, the column names will be used as the headers. Optional, only needed if 'DataUploaded' is set to False.\n 
        y: array, pandas Series. (default =''), shape = (n_samples,). Target values. If y is an array, the first value must be the header. If y is a pandas Series, the name of the Series will be used as the header. Optional, only needed if 'DataUploaded' is set to False.\n
        DataUploaded: boolean (default = True). If training data already uploaded to simMachines's software, set to True. If not, set to False and angels can be trained on new data not yet uploaded to the software by passing variables X and y to the classifier. \n
        FileName: string (default = ''). Name of the data file if new data is being used to train classifier. Optional, not needed if DataUploaded = True. \n
        specs: dictionary (default = {}). Data specification types for training data. Dictionary keys represent the header names, and the values represent the data types. Optional, highly recommended if DataUploaded = False. \n
        instanceName: string (default = ''), Name of instance to be trained.\n
        folderName: string (default = ''), Name of folder containing training data.\n
        specFileName: string (default = ''), Name of spec file to use for training. If empty, the most recent compatible file will be chosen.\n
        verbose: bool (default = True). Enable verbose output\n
        Pivots: int (default = 256), The number of primary search points in the engine. This may improve query speed at the cost of training time. (Range 256 to 1024)\n
        Probability: float (default = .95), Minimum accepted probability that the distance between the result and the query will be within the Accepted Error range.  Any result with lower probability will be discarded.\n
        AcceptedError: float (default = 1.2), Maximum accepted difference in distance between returned objects and the query object (Minimum = 1).\n
        Bins: int (default = 10), Specifies the number of ranges to be used in calculating the similarity of REAL columns.\n
        K: int (default = 10), Specify the k number of results for the nearest neighbor search.\n
        TopColumns: int (default = 20), The number of columns to consider for each prediction. Note that columns with strings, such as Multi_English, can be divided into multiple columns for this purpose.\n
        Length: int (default = 2), The total number of classes to consider for each prediction.\n
        DenseMode: string (default = 'SMART'), Sets the distance function used. Impacts weighting of factors (Also accepts: DEFAULT, MARQ3, EXCEEDS).\n
        EnergyWeight: bool (default = True), Useful if one classification is expected to be a significantly larger proportion of the results.\n
        Threshold: float (default = .5), The confidence level above which a class is considered an acceptable prediction. Non-default values are useful for unbalanced class distributions.\n
        ClassificationK: int (default = -1), Classifier K, the number of nearest neighbors used in making the classification (Default CK = Auto Detect).\n
        Iterations: int (default = 1000), Number of iterations of the metric learning algorithm. The learned metric may converge in fewer iterations. If so, the number will be displayed in grid and fold results.\n
        LearningRate: float (default = .1), Step size of the learning algorithm. Small values can lead to longer runtime. Large values can lead to overfitting. Lower Learning Rate values should be used if higher Iterations values are specified.\n
        FeatureSubsampling: float (default = 1.0), Ratio of randomly subsampled features at each iteration of the metric learning algorithm. Randomizations provides diversity in the preparation of the similarity criteria. A value of 1.0 means that all features are used in each iteration. Higher values can lead to slower training time and overfitting. A reasonable range is 0.01 to 0.3.\n
        FeatureFocus: int (default = 10), Maximum number of dynamically selected features at any given time. This works like a localized feature selection process. In each training iteration features are subsampled and within the subsample Feature Focus number of features are evaluated together to determine interaction. Higher values lead to slower training times and slower query times. Low values can lead to overfitting. \n
        ClassWeighting: string (default = 'UNIFORM'), Accepts 'UNIFORM' or 'NORMALIZED'. Uniform gives the same weight to all classes. Normalization takes into account class imbalance.\n
        Seed: int (default = 563131)\n
        Storage: int (default = 1)\n
        Parallelism: int (default = 2)\n
        PivotSampleSize: int (default = 20000)\n
        CacheSize: int (default = 1000000)\n
        IndexCount: int (default = 3)\n
        MaximumBytesPerObject: int (default = 500000)\n
        IndexSampleSize: int (default = 100)
        """
        
        ## Building base URL's
        base_cloud_url = 'https' + '://' + self.path + ':' + self.port + '/cloud' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud'
        self.base_cloud_url = base_cloud_url
        base_v2_url = 'https' + '://' + self.path + ':' + self.port + '/V2.0' if self.https else 'http' + '://' + self.path + ':' + self.port + '/V2.0'
        self.base_v2_url = base_v2_url
        
        ## Checking if folder exists
        if folderName:
            if instanceName:
                self.instanceName = instanceName
                if DataUploaded:
                    ## Warnings
                    if X:
                        raise Warning("Since 'DataUploaded' = True, 'X' will be ignored.")
                    if y:
                        raise Warning("Since 'Datauploaded' = True, 'y' will be ignored.")
                    if FileName:
                        raise Warning("Since 'DataUploaded' = True, 'FileName' will be ignored.")
                        
                    ## getting Specs from folder
                    specs_URL = self.base_cloud_url +'/listSpecByFolder?folderName=' + folderName
                    resp_specs = requests.get(specs_URL,auth=(self.username, self.b64password))
                    if resp_specs.status_code == 200:
                        specs_json = json.loads(resp_specs.content.decode())
                        columns_str = 'COLUMNS='
                        valid_specFileName = 0
                        createdDate = 0
                        for spec_file in specs_json['list']:
                            if 'LELIEL_ALJUNIED' in spec_file['angelName']:
                                if specFileName:
                                    if specFileName == spec_file['fileName']:
                                        valid_specFileName = 1
                                        for col in spec_file['specsMap'].keys():
                                            columnName = col
                                            specType = spec_file['specsMap'][col]
                                            columns_str += columnName + ':' + specType + ','
                                else:
                                    ## If specFileName not given by user, choose most 
                                    ## recent compatible file present 
                                    createdDate_curr = spec_file['createdDate']
                                    if createdDate_curr > createdDate:
                                        createdDate = createdDate_curr
                                        for col in spec_file['specsMap'].keys():
                                            columnName = col
                                            specType = spec_file['specsMap'][col]
                                            columns_str += columnName + ':' + specType + ','         
                    else:
                        raise AttributeError(resp_specs.content.decode())
                    
                    ## Error message if specFileName not recognized
                    if not valid_specFileName and specFileName:
                        raise AttributeError("Spec file name not recognized. Make sure to include file extension (.json, .tsv, etc.) in specFileName variable")
                ## New data not uploaded yet is being used to train angel
                else:
                    ## Warnings
                    if not specs:
                        raise Warning("Data type specifications ('specs') not provided. Automated specification types will be used in model creation. However, it is recommended that spec files are created by the user to improve model performence.")
                    
                    if specFileName:
                        raise Warning("A spec file name was provided for data not yet uploaded to aimMachines's software. 'specFileName' will be ignored.")

                    if isinstance(X,pd.DataFrame):
                        HeadersX = list(X.columns)
                        X = np.asarray(X)
                    elif isinstance(X,pd.Series):
                        HeadersX = [X.name]
                        X = np.asarray(X)
                    else:
                        if len(X) > 0:
                            HeadersX = list(X[0])
                            X = np.asarray(X)
                        else:
                            raise AttributeError('X must be provided if DataUploaded == False')
                            
                    if isinstance(y,pd.DataFrame):
                        HeaderY = list(y.columns)[0]
                        y = np.asarray(y)
                    elif isinstance(y,pd.Series):
                        HeaderY = y.name
                        y = np.asarray(y)
                    else:
                        if len(y) > 0:
                            HeaderY = list(y[0])
                            y = np.asarray(y)
                        else:
                            raise AttributeError('y must be provided if DataUploaded == False')   
                        
                    if not FileName:
                        raise AttributeError('Missing file name (FileName) for data to be uploaded.')

                    ## Create folder if "folderName" is not already created
                    listFolders_URL = self.base_cloud_url +'/listFolders'
                    resp_folders = requests.get(listFolders_URL,auth=(self.username, self.b64password))
                    if resp_folders.status_code == 200:
                        resp_folders_json = json.loads(resp_folders.content.decode())
                        folder_exists = 0
                        for item in resp_folders_json['list']:
                            if item['name'] == folderName:
                                folder_exists = 1
                    else:
                        raise AttributeError(resp_folders.content.decode())
                            
                    if not folder_exists:
                        createFolder_URL = self.base_cloud_url +'/createFolder'
                        folder_data = {"folderName" : folderName}
                        resp_CreateFolder = requests.post(createFolder_URL,data = folder_data,auth=(self.username, self.b64password))
                        if resp_CreateFolder.status_code == 200:
                            pass
                        else:
                            raise AttributeError(resp_CreateFolder.content.decode())
                    else:
                        raise AttributeError('Folder with name %s already exists.' % folderName)
                        
                    ## Upload data to "folderName"
                    uploadFile_URL = self.base_cloud_url + '/uploadFile'
                    ## Validating shape of input data
                    if X.shape[0] != y.shape[0]:
                        raise ValueError('X and y have incompatible shapes.')
                        
                    if X.shape[1] != len(HeadersX):
                        raise ValueError('X.shape[1] must equal the length of HeadersX')

                        
                    with open(FileName,'wb') as r:
                        ## Header
                        header_string = '\t'.join(HeadersX) + '\t' + str(HeaderY) + '\n'
                        r.write(header_string.encode('utf8'))
                        for i,row in enumerate(X):
                            row_str = '\t'.join([str(val) for val in row.tolist()]) + '\t' +str(y[i])
                            if i == (len(X)-1):
                                pass
                            else:
                                row_str += '\n'
                            r.write(row_str.encode('utf8'))
                        r.flush()
                    r.close()
                    
                    filesize = os.path.getsize(FileName)
                    
                    with open(FileName,'rb') as f:
                        file_stream = {'fileData' : f}
                        file_data = {'fileName' : FileName
                                  ,'fileSize' : filesize
                                  ,'folderName' : folderName
                                  ,'authorization' : self.filepassword
                                  }
                        resp_query = requests.post(uploadFile_URL
                                             ,files = file_stream
                                                  ,data = file_data
                                                  ,auth = (self.username, base64.b64decode(self.b64password).decode()))
                    f.close()
                    os.remove(FileName)
                    
                    if resp_query.status_code != 200:
                        raise AttributeError(resp_query.content.decode())
                    
                    ## Create spec file
                    columns_str = 'COLUMNS='
                    if not specs:
                        # Use recommended specs from /getSpecsOfFolder
                        getSpecs_URL = self.base_cloud_url + '/getSpecsOfFolder?folderName=' + folderName
                        resp_specs = requests.get(getSpecs_URL,auth=(self.username,self.b64password))
                        if resp_specs.status_code == 200:
                            resp_specs_json = json.loads(resp_specs.content.decode())
                            for item in resp_specs_json['columns']:
                                col_name = item['columnName']
                                if col_name == HeaderY:
                                    spec_type = 'CLASS'
                                else:
                                    spec_type = item['typeOfColumn']
                                columns_str += col_name + ':' + spec_type + ','
                        else:
                            raise AttributeError(resp_specs.content.decode())
                    else:
                        for item in specs.items():
                            col_name, spec_type = item
                            if col_name == HeaderY:
                                spec_type = 'CLASS'
                            columns_str += col_name + ':' + spec_type + ','
                            
                ## If number of neighbors specified, hardcode in the API string
                if ClassificationK == -1:
                    fixedK = '_@_@_FIXED_K=false'
                else:
                    fixedK = '_@_@_FIXED_K=true'
                    
                columns_str = columns_str[:-1]
                params_str = columns_str + '_@_@_K=' + str(K) + '_@_@_PIVOTS=' + str(Pivots) + '_@_@_PROBABILITY=' + str(Probability) + \
                            '_@_@_ACCEPTED_ERROR=' + str(AcceptedError) + '_@_@_TOP_COLUMNS=' + str(TopColumns) + '_@_@_DENSE_MODE=' + DenseMode + \
                            '_@_@_ENERGY_WEIGHT=' + EnergyWeight + '_@_@_THRESHOLD=' + str(Threshold) + '_@_@_BINS=' + str(Bins) + \
                            '_@_@_LENGTH=' + str(Length) + fixedK +'_@_@_CLASSIFICATION_K='  + str(ClassificationK) + '_@_@_ITERATIONS=' + str(Iterations) + \
                            '_@_@_LEARNING_RATE=' + str(LearningRate) + '_@_@_FEATURE_FOCUS=' + str(FeatureFocus) + '_@_@_CLASS_WEIGHTING=' + str(ClassWeighting) + \
                            '_@_@_FEATURE_SUBSAMPLING=' + str(FeatureSubsampling) + '_@_@_EXECUTE_FOLD=false' + '_@_@_PIVOT_SAMPLE_SIZE=' + \
                            str(PivotSampleSize) + '_@_@_CACHE_SIZE=' + str(CacheSize) + '_@_@_INDEX_COUNT=' + str(IndexCount) + '_@_@_MAXIMUM_BYTES_PER_OBJECT=' + \
                            str(MaximumBytesPerObject) + '_@_@_INDEX_SAMPLE_SIZE=' + str(IndexSampleSize) + '_@_@_SEED=' + str(Seed)
                ## Building API call
                instance_data = {"instanceName" : instanceName,
                                 "folderName" : folderName,
                                 "angelName": 'LELIEL_ALJUNIED',
                                 "params": params_str,
                                 "storage" : Storage,
                                 "parallelism" : Parallelism,
                                 "authorization" : self.filepassword
                        }
                ## POST request to create instance
                createInstance_url = self.base_cloud_url + '/createInstance'
                resp = requests.post(createInstance_url,data = instance_data, auth = (self.username, self.b64password))
                
                if resp.status_code == 200:
                    listInstances_url = self.base_cloud_url + '/listInstances'
                    status = 'Unknown'
                    while status not in ('RUNNNING', 'BUILD_ERROR'):
                        resp_status = requests.get(listInstances_url, auth=(self.username, self.b64password))
                        if resp_status.status_code == 200:
                            resp_JSON = json.loads(resp_status.content.decode())
                            
                            ## looping through instances
                            for l in resp_JSON['list']:
                                if l['label'] == self.instanceName:
                                    status_curr = l['status']
                                    if status != status_curr:
                                        status = status_curr
                                        if verbose:
                                            print('Status: ' + status)
                                        else:
                                            pass
                        else:
                            raise AttributeError(resp_status.content.decode())
                        if status == 'RUNNING':
                            print("Instance '" + self.instanceName + "' is ready for querying.")
                            break
                        elif status == 'BUILD_ERROR':
                            print("Instance '" + self.instanceName + "' returned a status of '" + status + "'.")
                            break
                else:
                    ## If instance not created, set instance name to '' 
                    self.instanceName = ''
                    raise AttributeError(resp.content.decode())
            else:
                raise AttributeError("Must enter instance name as 'instanceName' variable")
        else:
            raise AttributeError("Must specify name of folder to train Leliel with (folderName variable).")
        
        return self
    
        
    def predict(self, X,*, version = ''):
        """
        Predict using trained Leliel Aljunied instance, returns class.
        
        Parameters
        ----------
        X: {array-like}. Samples to predict. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        y_pred: array, shape = (n_samples,)
        Class labels for samples in X
        """
        
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            y_pred=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    sample_str = '\t'.join(samp)
                    queryObject_url = self.base_cloud_url + '/queryObject'
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryObject_url,data = query_data, auth = (self.username, self.b64password))
                    
                    if resp_query.status_code == 200:                     
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        winning_class = resp_query_json['winnerUsingThreshold']['predictedClass']
                        y_pred.append(winning_class)
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                        
                if not failed_queries:
                    return np.asarray(y_pred)
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")
                
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")
            
        
    def predict_confidence(self, X,*, version = ''):
        """
        Predict using trained Leliel Aljunied instance, returns confidence score.
        
        Parameters
        ----------
        X: {array-like}. Samples to predict. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        y_pred: array, shape = (n_samples,)
        Prediction confidence scores for samples in X
        """
        
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            y_pred=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    sample_str = '\t'.join(samp)
                    queryObject_url = self.base_cloud_url + '/queryObject'
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryObject_url,data = query_data, auth = (self.username, self.b64password))
                    
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        winning_score={}
                        for result in resp_query_json['results']:
                            winning_score[result['predictedClass']] = result['score']
                        y_pred.append(winning_score)
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                        
                if not failed_queries:
                    return np.asarray(y_pred)
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")
                
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")
            
    def get_factors(self, X,*, version = ''):
        """
        Returns local "Why" factors for each prediction.
        
        Parameters
        ----------
        X: {array-like}. Samples to predict. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        y_factors: array, shape = (n_samples,(n_features,3)
        Feature/value pairs, predictive weights, and boolean variable depicting if 
        feature/value pair is similar to the query object or not. This is 
        provided for each sample prediction in X.
        """
        if self.instanceName:
            headers_list = X[0]
            samples = X[1:]
            y_factors=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    data_dict = {}
                    for i,col in enumerate(headers_list):
                        data_dict[col] = samp[i]
                    queryFactors_url = self.base_v2_url + '/queryFactors'
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : data_dict,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : data_dict,
                                      "authorization" : self.filepassword
                                }
                    headers_api = {'Content-type': 'application/json'}
                    resp_query = requests.post(queryFactors_url,data = json.dumps(query_data), auth = (self.username, self.b64password),headers = headers_api)
                     
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        
                        ## Loop through query response, extract feature value pairs 
                        ## along with their local weights
                        feature_value_pairs=[]
                        weights=[]
                        similar_to_query=[]
                        for item in resp_query_json['featuresContribution']:
                            feature_value_pairs.append(item['colName']+'/'+str(item['value']))
                            weights.append(float(list(item['contributionByClass'].values())[0]))
                            similar_to_query.append(item['similarToQuery'])
                        y_factors.append(list(zip(feature_value_pairs,weights,similar_to_query)))
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                if not failed_queries:
                    return y_factors
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")              
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")           
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")        
            

class Ramiel():
    def __init__(self, **authenticate_creds):
        self.filepassword = authenticate_creds['filepassword']
        self.username = authenticate_creds['username']
        self.b64password = authenticate_creds['b64password']
        self.https = authenticate_creds['https']
        self.path = authenticate_creds['path']
        self.port = authenticate_creds['port']

        ## Second verification of username and password
        verify_URL = 'https' + '://' + self.path + ':' + self.port + '/cloud/verifyUser' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud/verifyUser'
        resp_verify = requests.get(verify_URL,auth=(self.username, self.b64password))
        if resp_verify.status_code != 200:
            raise AttributeError("Username-Password combination not recognized. Please try again.")

    def fit(self, * , X='', DataUploaded = True,FileName = '', specs={},
            instanceName = '',folderName = '', specFileName = '',verbose=True, Pivots = 256,
            Probability = .95, AcceptedError = 1.2, K = 10,
            Storage = 1, Parallelism = 2, PivotSampleSize = 20000, CacheSize = 1000000, 
            IndexCount = 3, MaximumBytesPerObject = 500000, IndexSampleSize = 100):

        """
        Train a Ramiel instance
        
        Parameters
        ----------
        X: array or pandas DataFrame (default = ''), shape = (n_samples, n_features). Training data. If X is an array, the first row must be the headers. If X is a pandas DataFrame, the column names will be used as the headers. Optional, only needed if 'DataUploaded' is set to False.\n 
        DataUploaded: boolean (default = True). If training data already uploaded to simMachines's software, set to True. If not, set to False and angels can be trained on new data not yet uploaded to the software by passing variables X and y to the classifier. \n
        FileName: string (default = ''). Name of the data file if new data is being used to train classifier. Optional, not needed if DataUploaded = True. \n
        specs: dictionary (default = {}). Data specification types for training data. Dictionary keys represent the header names, and the values represent the data types. Optional, highly recommended if DataUploaded = False. \n
        instanceName: string (default = ''), Name of instance to be trained.\n
        folderName: string (default = ''), Name of folder containing training data.\n
        specFileName: string (default = ''), Name of spec file to use for training. If empty, the most recent compatible file will be chosen.\n
        verbose: bool (default = True). Enable verbose output\n
        Pivots: int (default = 256), The number of primary search points in the engine. This may improve query speed at the cost of training time. (Range 256 to 1024)\n
        Probability: float (default = .95), Minimum accepted probability that the distance between the result and the query will be within the Accepted Error range.  Any result with lower probability will be discarded.\n
        AcceptedError: float (default = 1.2), Maximum accepted difference in distance between returned objects and the query object (Minimum = 1).\n
        K: int (default = 10), Specify the k number of results for the nearest neighbor search.\n
        Storage: int (default = 1)\n
        Parallelism: int (default = 2)\n
        PivotSampleSize: int (default = 20000)\n
        CacheSize: int (default = 1000000)\n
        IndexCount: int (default = 3)\n
        MaximumBytesPerObject: int (default = 500000)\n
        IndexSampleSize: int (default = 100)        
        """

        ## Building base URL's
        base_cloud_url = 'https' + '://' + self.path + ':' + self.port + '/cloud' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud'
        self.base_cloud_url = base_cloud_url
        base_v2_url = 'https' + '://' + self.path + ':' + self.port + '/V2.0' if self.https else 'http' + '://' + self.path + ':' + self.port + '/V2.0'
        self.base_v2_url = base_v2_url
        
        ## Checking if folder exists
        if folderName:
            if instanceName:
                self.instanceName = instanceName
                if DataUploaded:
                    ## Warnings
                    if X:
                        raise Warning("Since 'DataUploaded' = True, 'X' will be ignored.")
                    if FileName:
                        raise Warning("Since 'DataUploaded' = True, 'FileName' will be ignored.")
                    
                    ## getting Specs from folder
                    specs_URL = self.base_cloud_url +'/listSpecByFolder?folderName=' + folderName
                    resp_specs = requests.get(specs_URL,auth=(self.username, self.b64password))
                    if resp_specs.status_code == 200:
                        specs_json = json.loads(resp_specs.content.decode())
                        columns_str = 'COLUMNS='
                        valid_specFileName = 0
                        createdDate = 0
                        for spec_file in specs_json['list']:
                            if 'RAMIEL' in spec_file['angelName']:
                                if specFileName:
                                    if specFileName == spec_file['fileName']:
                                        valid_specFileName = 1
                                        for col in spec_file['specsMap'].keys():
                                            columnName = col
                                            specType = spec_file['specsMap'][col]
                                            columns_str += columnName + ':' + specType + ','
                                else:
                                    ## If specFileName not given by user, choose most 
                                    ## recent compatible file present 
                                    createdDate_curr = spec_file['createdDate']
                                    if createdDate_curr > createdDate:
                                        createdDate = createdDate_curr
                                        for col in spec_file['specsMap'].keys():
                                            columnName = col
                                            specType = spec_file['specsMap'][col]
                                            columns_str += columnName + ':' + specType + ','
                    else:
                        raise AttributeError(resp_specs.content.decode())
                    
                    ## Error message if specFileName not recognized
                    if not valid_specFileName and specFileName:
                        raise AttributeError("Spec file name not recognized. Make sure to include file extension (.json, .tsv, etc.) in specFileName variable")

                ## New data not uploaded yet is being used to train angel
                else:         
                    ## Warnings
                    if not specs:
                        raise Warning("Data type specifications ('specs') not provided. Automated specification types will be used in model creation. However, it is recommended that spec files are created by the user to improve model performence.")
                    
                    if specFileName:
                        raise Warning("A spec file name was provided for data not yet uploaded to aimMachines's software. 'specFileName' will be ignored.")
                    
                    if isinstance(X,pd.DataFrame):
                        HeadersX = list(X.columns)
                        X = np.asarray(X)
                    elif isinstance(X,pd.Series):
                        HeadersX = [X.name]
                        X = np.asarray(X)
                    else:
                        if len(X) > 0:
                            HeadersX = list(X[0])
                            X = np.asarray(X)
                        else:
                            raise AttributeError('X must be provided if DataUploaded == False')
                        
                    if not FileName:
                        raise AttributeError('Missing file name (FileName) for data to be uploaded.')

                    ## Create folder if "folderName" is not already created
                    listFolders_URL = self.base_cloud_url +'/listFolders'
                    resp_folders = requests.get(listFolders_URL,auth=(self.username, self.b64password))
                    if resp_folders.status_code == 200:
                        resp_folders_json = json.loads(resp_folders.content.decode())
                        folder_exists = 0
                        for item in resp_folders_json['list']:
                            if item['name'] == folderName:
                                folder_exists = 1
                    else:
                        raise AttributeError(resp_folders.content.decode())
                            
                    if not folder_exists:
                        createFolder_URL = self.base_cloud_url +'/createFolder'
                        folder_data = {"folderName" : folderName}
                        resp_CreateFolder = requests.post(createFolder_URL,data = folder_data,auth=(self.username, self.b64password))
                        if resp_CreateFolder.status_code == 200:
                            pass
                        else:
                            raise AttributeError(resp_CreateFolder.content.decode())
                    else:
                        raise AttributeError('Folder with name %s already exists.' % folderName)
                        
                    ## Upload data to "folderName"
                    uploadFile_URL = self.base_cloud_url + '/uploadFile'
                    
                    ## Validating shape of input data
                    if X.shape[1] != len(HeadersX):
                        raise ValueError('X.shape[1] must equal the length of HeadersX')

                        
                    with open(FileName,'wb') as r:
                        ## Header
                        header_string = '\t'.join(HeadersX) + '\n'
                        r.write(header_string.encode('utf8'))
                        for i,row in enumerate(X):
                            row_str = '\t'.join([str(val) for val in row.tolist()])
                            if i == (len(X)-1):
                                pass
                            else:
                                row_str += '\n'
                            r.write(row_str.encode('utf8'))
                        r.flush()
                    r.close()
                    
                    filesize = os.path.getsize(FileName)
                    
                    with open(FileName,'rb') as f:
                        file_stream = {'fileData' : f}
                        file_data = {'fileName' : FileName
                                  ,'fileSize' : filesize
                                  ,'folderName' : folderName
                                  ,'authorization' : self.filepassword
                                  }
                        resp_query = requests.post(uploadFile_URL
                                             ,files = file_stream
                                                  ,data = file_data
                                                  ,auth = (self.username, base64.b64decode(self.b64password).decode()))
                    f.close()
                    os.remove(FileName)
                    
                    if not resp_query.status_code == 200:
                        raise AttributeError(resp_query.content.decode())
                    
                    ## Create spec file
                    columns_str = 'COLUMNS='
                    if not specs:
                        # Use recommended specs from /getSpecsOfFolder
                        getSpecs_URL = self.base_cloud_url + '/getSpecsOfFolder?folderName=' + folderName
                        resp_specs = requests.get(getSpecs_URL,auth=(self.username,self.b64password))
                        if resp_specs.status_code == 200:
                            resp_specs_json = json.loads(resp_specs.content.decode())
                            for item in resp_specs_json['columns']:
                                col_name = item['columnName']
                                spec_type = item['typeOfColumn']
                                columns_str += col_name + ':' + spec_type + ','
                        else:
                            raise AttributeError(resp_specs_json.content.decode())
                    else:
                        for item in specs.items():
                            col_name, spec_type = item
                            columns_str += col_name + ':' + spec_type + ','
                            
                    
                columns_str = columns_str[:-1]
                params_str = columns_str + '_@_@_K=' + str(K) + '_@_@_PIVOTS=' + str(Pivots) + '_@_@_PROBABILITY=' + str(Probability) + \
                            '_@_@_ACCEPTED_ERROR=' + str(AcceptedError) + '_@_@_EXECUTE_FOLD=false' + '_@_@_PIVOT_SAMPLE_SIZE=' + \
                            str(PivotSampleSize) + '_@_@_CACHE_SIZE=' + str(CacheSize) + '_@_@_INDEX_COUNT=' + str(IndexCount) + '_@_@_MAXIMUM_BYTES_PER_OBJECT=' + \
                            str(MaximumBytesPerObject) + '_@_@_INDEX_SAMPLE_SIZE=' + str(IndexSampleSize)
                ## Building API call
                instance_data = {"instanceName" : instanceName,
                                 "folderName" : folderName,
                                 "angelName": 'RAMIEL',
                                 "params": params_str,
                                 "storage" : Storage,
                                 "parallelism" : Parallelism,
                                 "authorization" : self.filepassword
                        }
                ## POST request to create instance
                createInstance_url = self.base_cloud_url + '/createInstance'
                resp = requests.post(createInstance_url,data = instance_data, auth = (self.username, self.b64password))
                
                if resp.status_code == 200:
                    listInstances_url = self.base_cloud_url + '/listInstances'
                    status = 'Unknown'
                    while status not in ('RUNNNING', 'BUILD_ERROR'):
                        resp_status = requests.get(listInstances_url, auth=(self.username, self.b64password))
                        if resp_status.status_code == 200:
                            resp_JSON = json.loads(resp_status.content.decode())
                            
                            ## looping through instances
                            for l in resp_JSON['list']:
                                if l['label'] == self.instanceName:
                                    status_curr = l['status']
                                    if status != status_curr:
                                        status = status_curr
                                        if verbose:
                                            print('Status: ' + status)
                                        else:
                                            pass
                        else:
                            raise AttributeError(resp_status.content.decode())
                        if status == 'RUNNING':
                            print("Instance '" + self.instanceName + "' is ready for querying.")
                            break
                        elif status == 'BUILD_ERROR':
                            print("Instance '" + self.instanceName + "' returned a status of '" + status + "'.")
                            break
                else:
                    ## If instance not created, set instance name to '' 
                    self.instanceName = ''
                    raise AttributeError(resp.content.decode())
            else:
                raise AttributeError("Must enter instance name as 'instanceName' variable")
        else:
            raise AttributeError("Must specify name of folder to train Leliel with (folderName variable).")
        
        return self
    
        
    def get_neighbors(self, X, *, version = ''):
        """
        Retrive neighbors using trained Ramiel instance.
        
        Parameters
        ----------
        X: {array-like}. Samples to retrieve neighbors for. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        neighbors_final: list, shape = (n_samples,(K,2))
        ID, distance pairs of nearest neighbors
        """
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            neighbors_final=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    neighbors=[]
                    sample_str = '\t'.join(samp)
                    queryObject_url = self.base_cloud_url + '/queryObject'
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryObject_url,data = query_data, auth = (self.username, self.b64password))
                        
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        for item in resp_query_json['results']:
                            neighbors.append((item['id'],float(item['distance'])))
                        neighbors_final.append(neighbors)
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                
                if not failed_queries:
                    return neighbors_final
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")        
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")           
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")
            
class Gaghiel_G():
    def __init__(self, **authenticate_creds):
        self.filepassword = authenticate_creds['filepassword']
        self.username = authenticate_creds['username']
        self.b64password = authenticate_creds['b64password']
        self.https = authenticate_creds['https']
        self.path = authenticate_creds['path']
        self.port = authenticate_creds['port']

        ## Second verification of username and password
        verify_URL = 'https' + '://' + self.path + ':' + self.port + '/cloud/verifyUser' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud/verifyUser'
        resp_verify = requests.get(verify_URL,auth=(self.username, self.b64password))
        if resp_verify.status_code != 200:
            raise AttributeError("Username-Password combination not recognized. Please try again.")
            
    def fit(self, * ,X='', y='', DataUploaded = True,FileName = '', specs={},
            instanceName = '',folderName = '', specFileName = '',verbose=True, Pivots = 256,
            Probability = .95, AcceptedError = 1.2, K = 10,
            Storage = 1, Parallelism = 2, PivotSampleSize = 20000, CacheSize = 1000000, 
            IndexCount = 3, MaximumBytesPerObject = 500000, IndexSampleSize = 100, 
            RepeatItems = 'No', TopRecommendations = 10):
        """
        Train a Gaghiel_G instance
        
        Parameters
        ----------
        X: array or pandas DataFrame (default = ''), shape = (n_samples, n_features). Training data. If X is an array, the first row must be the headers. If X is a pandas DataFrame, the column names will be used as the headers. Optional, only needed if 'DataUploaded' is set to False.\n 
        y: array, pandas Series. (default =''), shape = (n_samples,). Target values. If y is an array, the first value must be the header. If y is a pandas Series, the name of the Series will be used as the header. Optional, only needed if 'DataUploaded' is set to False.\n
        DataUploaded: boolean (default = True). If training data already uploaded to simMachines's software, set to True. If not, set to False and angels can be trained on new data not yet uploaded to the software by passing variables X and y to the classifier. \n
        FileName: string (default = ''). Name of the data file if new data is being used to train classifier. Optional, not needed if DataUploaded = True. \n
        specs: dictionary (default = {}). Data specification types for training data. Dictionary keys represent the header names, and the values represent the data types. Optional, highly recommended if DataUploaded = False. \n
        instanceName: string (default = ''), Name of instance to be trained.\n
        folderName: string (default = ''), Name of folder containing training data.\n
        specFileName: string (default = ''), Name of spec file to use for training. If empty, the most recent compatible file will be chosen.\n
        verbose: bool (default = True). Enable verbose output\n
        Pivots: int (default = 256), The number of primary search points in the engine. This may improve query speed at the cost of training time. (Range 256 to 1024)\n
        Probability: float (default = .95), Minimum accepted probability that the distance between the result and the query will be within the Accepted Error range.  Any result with lower probability will be discarded.\n
        AcceptedError: float (default = 1.2), Maximum accepted difference in distance between returned objects and the query object (Minimum = 1).\n
        K: int (default = 10), Specify the k number of results for the nearest neighbor search.\n
        Storage: int (default = 1)\n
        Parallelism: int (default = 2)\n
        PivotSampleSize: int (default = 20000)\n
        CacheSize: int (default = 1000000)\n
        IndexCount: int (default = 3)\n
        MaximumBytesPerObject: int (default = 500000)\n
        IndexSampleSize: int (default = 100)\n
        RepeatItems: string (default = 'No'), Should items already part of the query object be returned? Also accepts 'Yes'.
        TopRecommendations: int (default = 10), The maximum number of recommendations to return.
        """

        ## Building base URL's
        base_cloud_url = 'https' + '://' + self.path + ':' + self.port + '/cloud' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud'
        self.base_cloud_url = base_cloud_url
        base_v2_url = 'https' + '://' + self.path + ':' + self.port + '/V2.0' if self.https else 'http' + '://' + self.path + ':' + self.port + '/V2.0'
        self.base_v2_url = base_v2_url
        
        ## Checking if folder exists
        if folderName:
            if instanceName:
                self.instanceName = instanceName
                if DataUploaded:
                    ## Warnings
                    if X:
                        raise Warning("Since 'DataUploaded' = True, 'X' will be ignored.")
                    if y:
                        raise Warning("Since 'Datauploaded' = True, 'y' will be ignored.")
                    if FileName:
                        raise Warning("Since 'DataUploaded' = True, 'FileName' will be ignored.")
                        
                    ## getting Specs from folder
                    specs_URL = self.base_cloud_url +'/listSpecByFolder?folderName=' + folderName
                    resp_specs = requests.get(specs_URL,auth=(self.username, self.b64password))
                    if resp_specs.status_code == 200:
                        specs_json = json.loads(resp_specs.content.decode())
                        columns_str = 'COLUMNS='
                        valid_specFileName = 0
                        createdDate = 0
                        for spec_file in specs_json['list']:
                            if 'GAGHIEL_G' in spec_file['angelName']:
                                if specFileName:
                                    if specFileName == spec_file['fileName']:
                                        valid_specFileName = 1
                                        for col in spec_file['specsMap'].keys():
                                            columnName = col
                                            specType = spec_file['specsMap'][col]
                                            columns_str += columnName + ':' + specType + ','
                                else:
                                    ## If specFileName not given by user, choose most 
                                    ## recent compatible file present 
                                    createdDate_curr = spec_file['createdDate']
                                    if createdDate_curr > createdDate:
                                        createdDate = createdDate_curr
                                        for col in spec_file['specsMap'].keys():
                                            columnName = col
                                            specType = spec_file['specsMap'][col]
                                            columns_str += columnName + ':' + specType + ','
                    else:
                        raise AttributeError(resp_specs.content.decode())
                    
                    ## Error message if specFileName not recognized
                    if not valid_specFileName and specFileName:
                        raise AttributeError("Spec file name not recognized. Make sure to include file extension (.json, .tsv, etc.) in specFileName variable")
                
                ## New data not uploaded yet is being used to train angel
                else:
                    ## Warnings
                    if not specs:
                        raise Warning("Data type specifications ('specs') not provided. Automated specification types will be used in model creation. However, it is recommended that spec files are created by the user to improve model performence.")
                    
                    if specFileName:
                        raise Warning("A spec file name was provided for data not yet uploaded to aimMachines's software. 'specFileName' will be ignored.")
                    
                    if isinstance(X,pd.DataFrame):
                        HeadersX = list(X.columns)
                        X = np.asarray(X)
                    elif isinstance(X,pd.Series):
                        HeadersX = [X.name]
                        X = np.asarray(X)
                    else:
                        if len(X) > 0:
                            HeadersX = list(X[0])
                            X = np.asarray(X)
                        else:
                            raise AttributeError('X must be provided if DataUploaded == False')
                            
                    if isinstance(y,pd.DataFrame):
                        HeaderY = list(y.columns)[0]
                        y = np.asarray(y)
                    elif isinstance(y,pd.Series):
                        HeaderY = y.name
                        y = np.asarray(y)
                    else:
                        if len(y) > 0:
                            HeaderY = list(y[0])
                            y = np.asarray(y)
                        else:
                            raise AttributeError('y must be provided if DataUploaded == False')   
                        
                    if not FileName:
                        raise AttributeError('Missing file name (FileName) for data to be uploaded.')

                    ## Create folder if "folderName" is not already created
                    listFolders_URL = self.base_cloud_url +'/listFolders'
                    resp_folders = requests.get(listFolders_URL,auth=(self.username, self.b64password))
                    if resp_folders.status_code == 200:
                        resp_folders_json = json.loads(resp_folders.content.decode())
                        folder_exists = 0
                        for item in resp_folders_json['list']:
                            if item['name'] == folderName:
                                folder_exists = 1
                    else:
                        raise AttributeError(resp_folders.content.decode())
                            
                    if not folder_exists:
                        createFolder_URL = self.base_cloud_url +'/createFolder'
                        folder_data = {"folderName" : folderName}
                        resp_CreateFolder = requests.post(createFolder_URL,data = folder_data,auth=(self.username, self.b64password))
                        if resp_CreateFolder.status_code == 200:
                            pass
                        else:
                            raise AttributeError(resp_CreateFolder.content.decode())
                    else:
                        raise AttributeError('Folder with name %s already exists.' % folderName)
                        
                    ## Upload data to "folderName"
                    uploadFile_URL = self.base_cloud_url + '/uploadFile'
                    ## Validating shape of input data
                    if X.shape[0] != y.shape[0]:
                        raise ValueError('X and y have incompatible shapes.')
                        
                    if X.shape[1] != len(HeadersX):
                        raise ValueError('X.shape[1] must equal the length of HeadersX')

                        
                    with open(FileName,'wb') as r:
                        ## Header
                        header_string = '\t'.join(HeadersX) + '\t' + str(HeaderY) + '\n'
                        r.write(header_string.encode('utf8'))
                        for i,row in enumerate(X):
                            row_str = '\t'.join([str(val) for val in row.tolist()]) + '\t' +str(y[i])
                            if i == (len(X)-1):
                                pass
                            else:
                                row_str += '\n'
                            r.write(row_str.encode('utf8'))
                        r.flush()
                    r.close()
                    
                    filesize = os.path.getsize(FileName)
                    
                    with open(FileName,'rb') as f:
                        file_stream = {'fileData' : f}
                        file_data = {'fileName' : FileName
                                  ,'fileSize' : filesize
                                  ,'folderName' : folderName
                                  ,'authorization' : self.filepassword
                                  }
                        resp_query = requests.post(uploadFile_URL
                                             ,files = file_stream
                                                  ,data = file_data
                                                  ,auth = (self.username, base64.b64decode(self.b64password).decode()))
                    f.close()
                    os.remove(FileName)
                    
                    if not resp_query.status_code == 200:
                        raise AttributeError(resp_query.content.decode())
                    
                    ## Create spec file
                    columns_str = 'COLUMNS='
                    if not specs:
                        # Use recommended specs from /getSpecsOfFolder
                        getSpecs_URL = self.base_cloud_url + '/getSpecsOfFolder?folderName=' + folderName
                        resp_specs = requests.get(getSpecs_URL,auth=(self.username,self.b64password))
                        if resp_specs.status_code == 200:
                            resp_specs_json = json.loads(resp_specs.content.decode())
                            for item in resp_specs_json['columns']:
                                col_name = item['columnName']
                                if col_name == HeaderY:
                                    spec_type = 'CLASS_ITEM_SET'
                                else:
                                    spec_type = item['typeOfColumn']
                                columns_str += col_name + ':' + spec_type + ','
                        else:
                            raise AttributeError(resp_specs.content.decode())
                    else:
                        for item in specs.items():
                            col_name, spec_type = item
                            if col_name == HeaderY:
                                spec_type = 'CLASS_ITEM_SET'
                            columns_str += col_name + ':' + spec_type + ','                    


                columns_str = columns_str[:-1]
                params_str = columns_str + '_@_@_K=' + str(K) + '_@_@_PIVOTS=' + str(Pivots) + '_@_@_PROBABILITY=' + str(Probability) + \
                            '_@_@_ACCEPTED_ERROR=' + str(AcceptedError) + '_@_@_EXECUTE_FOLD=false' + '_@_@_PIVOT_SAMPLE_SIZE=' + \
                            str(PivotSampleSize) + '_@_@_CACHE_SIZE=' + str(CacheSize) + '_@_@_INDEX_COUNT=' + str(IndexCount) + '_@_@_MAXIMUM_BYTES_PER_OBJECT=' + \
                            str(MaximumBytesPerObject) + '_@_@_INDEX_SAMPLE_SIZE=' + str(IndexSampleSize) + '_@_@_REPEAT_ITEMS=' \
                            + str(RepeatItems) + '_@_@_TOP_RECOMMENDATIONS=' + str(TopRecommendations)
                ## Building API call
                instance_data = {"instanceName" : instanceName,
                                 "folderName" : folderName,
                                 "angelName": 'GAGHIEL_G',
                                 "params": params_str,
                                 "storage" : Storage,
                                 "parallelism" : Parallelism,
                                 "authorization" : self.filepassword
                        }
                ## POST request to create instance
                createInstance_url = self.base_cloud_url + '/createInstance'
                resp = requests.post(createInstance_url,data = instance_data, auth = (self.username, self.b64password))
                
                if resp.status_code == 200:
                    listInstances_url = self.base_cloud_url + '/listInstances'
                    status = 'Unknown'
                    while status not in ('RUNNNING', 'BUILD_ERROR'):
                        resp_status = requests.get(listInstances_url, auth=(self.username, self.b64password))
                        if resp_status.status_code == 200:
                            resp_JSON = json.loads(resp_status.content.decode())
                            
                            ## looping through instances
                            for l in resp_JSON['list']:
                                if l['label'] == self.instanceName:
                                    status_curr = l['status']
                                    if status != status_curr:
                                        status = status_curr
                                        if verbose:
                                            print('Status: ' + status)
                                        else:
                                            pass
                        else:
                            raise AttributeError(resp_status.content.decode())
                        if status == 'RUNNING':
                            print("Instance '" + self.instanceName + "' is ready for querying.")
                            break
                        elif status == 'BUILD_ERROR':
                            print("Instance '" + self.instanceName + "' returned a status of '" + status + "'.")
                            break
                else:
                    ## If instance not created, set instance name to '' 
                    self.instanceName = ''
                    raise AttributeError(resp.content.decode())
            else:
                raise AttributeError("Must enter instance name as 'instanceName' variable")
        else:
            raise AttributeError("Must specify name of folder to train Leliel with (folderName variable).")
        
        return self
        
    def predict(self, X, *, version = ''):
        """
        Predict using a Gaghiel_G instance.
        
        Parameters
        ----------
        X: {array-like}. Samples to predict. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        y_pred: list, shape = (n_samples,(K,2))
        Item, weight pairs of recommendations
        """
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            y_pred=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    sample_str = '\t'.join(samp)
                    queryObject_url = self.base_cloud_url + '/queryObject'
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryObject_url,data = query_data, auth = (self.username, self.b64password))
                              
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        items=[]
                        weights=[]
                        for item in resp_query_json['results']:
                            items.append(item['id'])
                            weights.append(float(item['weight']))
                        y_pred.append(list(zip(items,weights)))
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()                            
                if not failed_queries:
                    return y_pred
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")            
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")              
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")        
    def get_neighbors(self, X, *, version = ''):
        """
        Retrive neighbors using trained Gaghiel_G instance.
        
        Parameters
        ----------
        X: {array-like}. Samples to retrieve neighbors for. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        neighbors_final: list of dictionaries, shape = (n_samples,(Classification K * TopRecommendations,2))
        ID, distance pairs of nearest neighbors
        """
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            neighbors_final=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    sample_str = '\t'.join(samp)
                    # print sample_str
                    queryObject_url = self.base_cloud_url + '/queryVisualization'            
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryObject_url,data = query_data, auth = (self.username, self.b64password))
                            
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        
                        ## Extracting neighbors for each class, sorting by distance 
                        ## in ascending order regardless of class
                        neighbors_dict={}
                        for class_ in resp_query_json['listMap'].keys():
                            distance_l=[]
                            id_l=[]
                            for neighbor in resp_query_json['listMap'][class_]['queryRelatedObject']:
                                distance = neighbor['distance']
                                objectId = neighbor['objectId']
                                distance_l.append(distance)
                                id_l.append(objectId)
                            neighbors = [(id_0,float(dist)) for dist,id_0 in sorted(zip(distance_l,id_l),reverse=False)]
                            neighbors_dict[class_] = neighbors
                        neighbors_final.append(neighbors_dict)
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                if not failed_queries:
                    return neighbors_final
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")  
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")           
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")        
        
    def get_factors(self, X, *, version = ''):
        """
        Returns local "Why" factors for each prediction.
        
        Parameters
        ----------
        X: {array-like}. Samples to predict. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        y_factors: array, shape = (n_samples,(n_features,3)
        Feature/value pairs, predictive weights, and boolean variable depicting if 
        feature/value pair is similar to the query object or not. This is 
        provided for each sample prediction in X.
        """
        if self.instanceName:
            headers = X[0]
            headers_str = '\t'.join(headers)
            samples = X[1:]
            y_factors=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    sample_str = '\t'.join(samp)
                    queryVisualization_url = self.base_cloud_url + '/queryVisualization'            
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryVisualization_url,data = query_data, auth = (self.username, self.b64password))
                                    
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        predicted_classes = [item['id'] for item in resp_query_json['rawQueryResponse']['results']]
                        
                        ## Loop through query response, extract feature value pairs 
                        ## along with their local weights for predicted class
                        y_factors_dict={}
                        for predicted_class in predicted_classes:
                            feature_value_pairs=[]
                            weights=[]
                            similar_to_query=[]
                            for item in resp_query_json['listMap'][predicted_class]['globalQueryObjects']:
                                feature_value_pairs.append(item['matchedItem'])
                                weights.append(float(item['weight']))
                                similar_to_query.append(item['similarToQuery'])
                            factors_sorted = sorted(zip(weights,feature_value_pairs,similar_to_query),reverse=True)
                            y_factors_dict[predicted_class] = [(feature,weight,similar) for weight,feature,similar in factors_sorted]
                        y_factors.append(y_factors_dict)
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                
                if not failed_queries:
                    return y_factors
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")           
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")