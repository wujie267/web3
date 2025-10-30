import streamlit as st
import pandas as pd
import plotly.express as px

def get_dataframe_from_excel():
    # 修复Excel读取相关的语法错误
    df = pd.read_excel(
        'supermarket_sales.xlsx',
        sheet_name='销售数据',  # 修复引号和中文逗号错误
        skiprows=1,
        index_col='订单号'
    )  # 修复缺少的右括号
    # 提取小时数
    df['小时数'] = pd.to_datetime(df["时间"], format="%H:%M:%S").dt.hour
    return df

def add_sidebar_func(df):
    with st.sidebar:
        st.header("请筛选数据：")
        
        # 城市筛选
        city_unique = df["城市"].unique()
        city = st.multiselect(
            "请选择城市：",
            options=city_unique,
            default=city_unique,  # 修复语法错误
        )
        
        # 顾客类型筛选
        customer_type_unique = df["顾客类型"].unique()  # 修复赋值符号错误
        customer_type = st.multiselect(
            "请选择顾客类型：",
            options=customer_type_unique,  # 修复参数符号错误
            default=customer_type_unique,
        )
        
        # 性别筛选
        gender_unique = df["性别"].unique()
        gender = st.multiselect(
            "请选择性别：",  # 补充冒号
            options=gender_unique,
            default=gender_unique,
        )
        
        # 根据筛选条件过滤数据
        df_selection = df.query(
            "城市 == @city & 顾客类型 == @customer_type & 性别 == @gender"
        )
        return df_selection

def product_line_chart(df):
    # 按产品类型汇总销售额
    sales_by_product_line = (
        df.groupby(by=["产品类型"])[["总价"]].sum().sort_values(by="总价")
    )
    # 创建水平条形图
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="总价",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>按产品类型划分的销售额</b>",
    )  # 修复缺少的右括号
    return fig_product_sales  # 修复变量名错误和空格错误

def hour_chart(df):
    # 按小时汇总销售额
    sales_by_hour = df.groupby(by=["小时数"])[["总价"]].sum()
    # 创建条形图
    fig_hour_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="总价",
        title="<b>按小时数划分的销售额</b>",
    )  # 修复缺少的右括号
    return fig_hour_sales  # 修复返回语句错误

def main_page_demo(df):
    """主界面函数"""
    st.title(':bar_chart: 销售仪表板')  # 修复中文冒号错误
    
    # 计算关键指标
    total_sales = int(df["总价"].sum())
    average_rating = round(df["评分"].mean(), 1)
    star_rating_string = ":star:" * int(round(average_rating, 0))
    average_sale_by_transaction = round(df["总价"].mean(), 2)  # 修复列名错误
    
    # 显示关键指标
    left_key_col, middle_key_col, right_key_col = st.columns(3)
    with left_key_col:
        st.subheader("总销售额：")
        st.subheader(f"RMB ¥ {total_sales:,}")  # 修复格式化错误
    
    with middle_key_col:
        st.subheader("顾客评分的平均值：")
        st.subheader(f"{average_rating} {star_rating_string}")  # 修复格式化错误
    
    with right_key_col:
        st.subheader("每单的平均销售额：")
        st.subheader(f"RMB ¥ {average_sale_by_transaction}")  # 修复格式化错误
    
    st.divider()
    
    # 显示图表
    left_chart_col, right_chart_col = st.columns(2)
    with left_chart_col:
        hour_fig = hour_chart(df)
        st.plotly_chart(hour_fig, use_container_width=True)
    
    with right_chart_col:
        product_fig = product_line_chart(df)
        st.plotly_chart(product_fig, use_container_width=True)

def run_app():
    """启动应用"""
    st.set_page_config(
        page_title="销售仪表板",
        page_icon=":bar_chart:",
        layout="wide"
    )
    
    # 读取数据
    sale_df = get_dataframe_from_excel()
    # 获取筛选后的数据
    df_selection = add_sidebar_func(sale_df)
    # 显示主页面
    main_page_demo(df_selection)

# 主程序入口
if __name__ == "__main__":  # 修复语法错误
    run_app()
