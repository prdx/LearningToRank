import pandas as pd
from sklearn.linear_model import LinearRegression

df_train = pd.read_csv("./matrix_train.csv", header=None)
df_train_x = df_train.iloc[:,2:7]
df_train_y = df_train.iloc[:,-1]
q_id_train = df_train.iloc[:,1]
doc_id_train = df_train.iloc[:,0]

regressor = LinearRegression()
regressor.fit(df_train_x, df_train_y)

df_test = pd.read_csv("./matrix_test.csv", header=None)
df_test_x = df_test.iloc[:,2:7]
df_test_y = df_test.iloc[:,-1]
y_pred = regressor.predict(df_test_x)
q_id_test = df_test.iloc[:,1]
doc_id_test = df_test.iloc[:,0]

q_id_test_distinct = set(q_id_test)

df = pd.DataFrame({'Q_Id': q_id_test, 'Doc_Id': doc_id_test, 'Actual': df_test_y, 'Predicted': y_pred})
sorted_df = df.sort_values(by=['Q_Id', 'Predicted'], ascending=False).groupby('Q_Id').head(1000)

with open("test_eval.txt", "w") as test_eval:
    rank = 1
    for index, row in sorted_df.iterrows():
        string = "{0} Q0 {1} {2} {3} Exp\n".format(row['Q_Id'], row['Doc_Id'], rank, row['Predicted'])
        test_eval.write(string)
        if rank == 1000:
            rank = 0
        rank += 1


y_pred = regressor.predict(df_train_x)
df = pd.DataFrame({'Q_Id': q_id_train, 'Doc_Id': doc_id_train, 'Actual': df_train_y, 'Predicted': y_pred})
sorted_df = df.sort_values(by=['Q_Id', 'Predicted'], ascending=False).groupby('Q_Id').head(1000)

with open("train_eval.txt", "w") as test_eval:
    rank = 1
    for index, row in sorted_df.iterrows():
        string = "{0} Q0 {1} {2} {3} Exp\n".format(row['Q_Id'], row['Doc_Id'], rank, row['Predicted'])
        test_eval.write(string)
        if rank == 1000:
            rank = 0
        rank += 1
