import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud #绘制词云图
import jieba    #分词处理
from PIL import Image

plt.rcParams['font.sans-serif']='SimHei'
plt.rcParams['axes.unicode_minus']=False
df = pd.read_csv("../bilibili淄博评论爬取.csv")
#柱状图
def bar():
    data = df.value_counts("ip属地").nlargest(10)
    #df.value_counts("ip属地").nlargest(10).plot(kind="bar",figsize=(8,5),grid=True)
    data.plot.bar(figsize=(8,5),grid=True)
    plt.title("IP属地TOP10统计-柱状图")#标题
    plt.xticks(rotation=0)#x轴标签位置横向
    plt.xlabel("")#x轴名称
    plt.ylabel("占比")#y轴名称
    #设置柱状图每个柱的值，使用.annotate()函数
    for i,value in enumerate(data):
        plt.annotate(str(value),xy=(i,value),ha="center",va="bottom")

    plt.savefig("../IP属地TOP10统计-柱状图.png",dpi=300)  #保存为图片
    plt.show()
    plt.close()
#折线图
def line():
    df["评论时间2"] = pd.to_datetime(df["评论时间"])#将输入的容器时间格式的数据转为Pandas中的Datetime对象
    df["评论日期"] = df["评论时间2"].dt.date   #.dt.date是'Series'或'DataFrame'对象的属性,可以将Datetime对象提取出年、月、日转为日期格式
    df_count_date = df["评论日期"].value_counts()   #分组,则列名会分为"评论日期"和"count"
    df_count_date = df_count_date.reset_index()
    df_count_date.columns = ["评论日期","评论数量"]    #将列名重新设置为"评论日期"和"评论数量",因为日期有多少个,说明评论了多少次
    # 因为数据太多,x轴坐标年月日格式会被缩减为年月
    df_count_date.plot(x="评论日期",y="评论数量",figsize=(9,4),grid=True)
    #折线图上最大值显示
    max_value = df_count_date["评论数量"].max() #获取"评论数量"列的最大值
    max_value_index = df_count_date["评论数量"].idxmax()    #获取"评论数量"列的最大值的索引
    max_value_date= df_count_date.loc[max_value_index,"评论日期"]   #根据"评论数量"列的最大值的索引来获取"评论日期"列的值
    plt.annotate(max_value_date,xy=(max_value_date,max_value), xytext=(-20, 25),
            textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
    #折线图上最小值显示
    min_value = df_count_date["评论数量"].min()
    min_value_index = df_count_date["评论数量"].idxmin()
    min_value_date = df_count_date.loc[min_value_index, "评论日期"]
    plt.annotate(min_value_date, xy=(min_value_date, min_value), xytext=(-20, 25),
                 textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
    plt.title("评论数量统计-折线图")
    import matplotlib.dates as mdates
    #plt.gca()获取坐标轴对象,.xaxis表示获取当前坐标轴的x轴属性,后续的表示设置x轴刻度的格式为'%Y-%m-%d'
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))#折线图因为数据多,x轴日期被缩减为年月,这里设置x轴刻度的格式为'%Y-%m-%d',没有%d则会设置为01
    plt.savefig("../评论数量统计-折线图.png", dpi=200)  # 保存为图片
    plt.show()
    plt.close()
#箱线图
def box():
    #因为点赞数很多，我们取大于500的点赞数来查看分布
    date = df[df["点赞数"] >= 500]
    #.values是根据类型将序列返回为numpy.ndarray类型；.tolist()是转为list类型
    date2 = date["点赞数"].values.tolist()
    plt.figure(figsize=(9,4))
    plt.boxplot(date2,labels=['点赞分布'])
    plt.ylabel("点赞数")
    plt.title = "点赞数分布-箱线图"
    plt.savefig("../点赞数分布-箱线图.png", dpi=200)  # 保存为图片
    plt.show()
    plt.close()
#绘制词云
def wordloud():
    #将评论内容写到.text文本,为后续绘制词云做准备
    date = df["点赞数"].sort_values(ascending=False)  # 降序
    with open('评论内容.text', 'w', encoding='utf-8') as f:
        for index in date[:100].index:
            text = df.loc[index, "评论内容"]
            f.write(text + '\n')
    #哈工大停用词
    with open('hit_stopwords.txt', 'r', encoding='utf8') as f:
        stopwords_list = f.readlines()
    stopwords_list = [i.strip() for i in stopwords_list]
    excludes = ['我', '的', '啊', '了', '不', '去', '没', '不是','不要','更','大家', '都', '没有', '人', '现在', '很', '还', '说','真的']
    stopwords_list.extend(excludes)    #还可以在这列表中添加停用词数据
    #对文本进行分词,并使用空格来拼接分词,因为wordcloud默认会以空格为分隔符对目标文本进行分词处理,所以下面使用空格来进行分词拼接处理
    with open('评论内容.text', 'r', encoding='utf8') as f:
        text2 = ' '.join(jieba.cut(f.read()))
    #绘制云图
    mask = np.array(Image.open("masking.png"))  # 设置蒙版
    wc = WordCloud(font_path="C:\Windows\Fonts\simhei.ttf", stopwords=stopwords_list,mask=mask)
    generate_text = wc.generate(text2)  # WordCloud对象中加载文本
    plt.imshow(generate_text, interpolation='bilinear')  # 绘制处图像
    plt.axis("off")  # 不显示xy轴
    plt.show()  # 显示图像
    wc.to_file('../中文词云图.jpg')    #或者直接输出保存图像



if __name__ == '__main__':
    bar()
    line()
    box()
    wordloud()


