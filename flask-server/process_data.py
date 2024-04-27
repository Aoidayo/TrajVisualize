import pandas as pd

df = pd.read_csv("./data/913155_qgis_res_LinearSim_porto_256_knn.csv")

def process_queryId():
    tmp = df.copy()['class'].unique()
    df_unique_classes = pd.DataFrame({'class': tmp})
    df_unique_classes.to_csv('unique_classes.csv', index=False)

# process_queryId()

# df = pd.read_csv("./data/unique_classes.csv")
# def process_pre_100():
#     tmp = pd.DataFrame(columns=["index","id","wkt","class"])
#     df = pd.read_csv

def save_pre_100():
    tmp = df[:1200]
    tmp.to_csv("./data/pre100.csv",index=False)
save_pre_100()