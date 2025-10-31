from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
import time

class FreeTrendAnalyzer:
    def __init__(self):
        """初始化,添加更稳定的配置"""
        try:
            self.pytrend = TrendReq(
                hl='en-US',
                tz=360,
                timeout=(10, 25),
                retries=2,
                backoff_factor=0.1,
                requests_args={'verify': True}  # 添加SSL验证
            )
            print(" pytrends 初始化成功")
        except Exception as e:
            print(f" 初始化失败: {e}")
         
            raise
    
    def get_trend_data(self, keywords, timeframe='today 12-m', geo=''):
        """
        获取搜索趋势数据(带错误处理)
        
        参数:
        - keywords: 列表,最多5个关键词
        - timeframe: 'today 12-m', 'today 3-m', 'now 7-d' 等
        - geo: 地区代码 (''=全球, 'US'=美国, 'CN'=中国)
        """
        try:
            # 限制关键词数量
            if len(keywords) > 5:
                print(f"⚠️ 关键词过多({len(keywords)}),只取前5个")
                keywords = keywords[:5]
            
            print(f"🔍 正在查询: {keywords}")
            
            self.pytrend.build_payload(
                kw_list=keywords,
                cat=0,
                timeframe=timeframe,
                geo=geo,
                gprop=''
            )
            
            # 获取数据
            interest_over_time = self.pytrend.interest_over_time()
            
            if interest_over_time.empty:
                print("⚠️ 未找到数据(可能关键词搜索量太低)")
                return pd.DataFrame()
            
            # 移除 'isPartial' 列
            if 'isPartial' in interest_over_time.columns:
                interest_over_time = interest_over_time.drop('isPartial', axis=1)
            
            print(f"✅ 成功获取 {len(interest_over_time)} 条数据")
            return interest_over_time
            
        except Exception as e:
            print(f"❌ 查询失败: {e}")
            return pd.DataFrame()
    
    def get_related_queries(self, keyword):
        """获取相关搜索查询"""
        try:
            self.pytrend.build_payload([keyword], timeframe='today 12-m')
            related = self.pytrend.related_queries()
            
            return {
                'rising': related[keyword]['rising'],
                'top': related[keyword]['top']
            }
        except Exception as e:
            print(f"❌ 获取相关查询失败: {e}")
            return {'rising': None, 'top': None}
    
    def safe_analyze(self, keyword, delay=2):
        """
       
        参数:
        - delay: 请求间隔(秒)
        """
        results = {}
        
        # 1. 趋势数据
        print(f"\n{'='*60}")
        print(f"📊 分析关键词: {keyword}")
        print(f"{'='*60}")
        
        trend_data = self.get_trend_data([keyword])
        if not trend_data.empty:
            results['avg_interest'] = trend_data[keyword].mean()
            results['max_interest'] = trend_data[keyword].max()
            results['current_trend'] = '📈 上升' if trend_data[keyword].iloc[-1] > trend_data[keyword].iloc[0] else '📉 下降'
            print(f"平均热度: {results['avg_interest']:.1f}")
            print(f"最高热度: {results['max_interest']}")
            print(f"趋势方向: {results['current_trend']}")
        
        time.sleep(delay)  # 延迟避免封禁
        
        # 2. 相关查询
        print(f"\n🔗 相关查询...")
        related = self.get_related_queries(keyword)
        if related['rising'] is not None:
            results['rising_queries'] = related['rising']['query'].head(5).tolist()
            print("上升查询:")
            for q in results['rising_queries']:
                print(f"  • {q}")
        
        return results




def test_pytrends():
    """测试ZBAA文章的10个SEO关键词"""
    print("🚀 开始分析ZBAA SEO关键词趋势\n")
    
    try:
        analyzer = FreeTrendAnalyzer()
        
        # 定义10个关键词（按策略分组）
        primary_keywords = [
            "private jet charter Beijing",
            "business aviation Beijing",
            "private jet rental China"
        ]

        secondary_keywords = [
            "Beijing to Shanghai private jet",
            "Beijing Hong Kong charter flight",
            "executive jet China",
            "business jet charter Asia"
        ]

        longtail_keywords = [
            "how much private jet Beijing to Hong Kong",
            "best private jet for long distance flights",
            "VIP flight service Beijing airport"
        ]
        
        all_keywords = primary_keywords + secondary_keywords + longtail_keywords
        
        # 存储结果
        results_summary = []
        
        print("="*80)
        print("第一部分：主要关键词分析（Primary Keywords）")
        print("="*80)
        
        for i, keyword in enumerate(primary_keywords, 1):
            print(f"\n[{i}/10] 分析: {keyword}")
            result = analyzer.safe_analyze(keyword, delay=3)
            if result:
                results_summary.append({
                    'keyword': keyword,
                    'type': 'Primary',
                    'avg_interest': result.get('avg_interest', 0),
                    'trend': result.get('current_trend', 'N/A')
                })
            time.sleep(3)
        
        print("\n" + "="*80)
        print("第二部分：次要关键词分析（Secondary Keywords）")
        print("="*80)
        
        for i, keyword in enumerate(secondary_keywords, 4):
            print(f"\n[{i}/10] 分析: {keyword}")
            result = analyzer.safe_analyze(keyword, delay=3)
            if result:
                results_summary.append({
                    'keyword': keyword,
                    'type': 'Secondary',
                    'avg_interest': result.get('avg_interest', 0),
                    'trend': result.get('current_trend', 'N/A')
                })
            time.sleep(3)
        
        print("\n" + "="*80)
        print("第三部分：长尾关键词分析（Long-tail Keywords）")
        print("="*80)
        
        for i, keyword in enumerate(longtail_keywords, 8):
            print(f"\n[{i}/10] 分析: {keyword}")
            result = analyzer.safe_analyze(keyword, delay=3)
            if result:
                results_summary.append({
                    'keyword': keyword,
                    'type': 'Long-tail',
                    'avg_interest': result.get('avg_interest', 0),
                    'trend': result.get('current_trend', 'N/A')
                })
            time.sleep(3)
        
        # 生成对比分析报告
        print("\n" + "="*80)
        print("📊 关键词热度对比总结")
        print("="*80)
        
        if results_summary:
            df_results = pd.DataFrame(results_summary)
            df_results = df_results.sort_values('avg_interest', ascending=False)
            
            print(f"\n{'排名':<5} {'关键词':<50} {'类型':<12} {'平均热度':<10} {'趋势'}")
            print("-" * 90)
            
            for idx, row in df_results.iterrows():
                print(f"{df_results.index.get_loc(idx)+1:<5} {row['keyword']:<50} {row['type']:<12} {row['avg_interest']:<10.1f} {row['trend']}")
            
            # 按类型分组统计
            print("\n" + "="*80)
            print("📈 按类型分组分析")
            print("="*80)
            
            type_stats = df_results.groupby('type')['avg_interest'].agg(['mean', 'max', 'min'])
            print(f"\n{'关键词类型':<15} {'平均热度':<12} {'最高热度':<12} {'最低热度'}")
            print("-" * 55)
            for kw_type, stats in type_stats.iterrows():
                print(f"{kw_type:<15} {stats['mean']:<12.1f} {stats['max']:<12.1f} {stats['min']:<12.1f}")
        
        # 额外测试：对比核心关键词组（Google Trends限制5个）
        print("\n" + "="*80)
        print("🔥 核心关键词直接对比（Top 5）")
        print("="*80)
        
        top_5_keywords = [
            "private jet charter Beijing",
            "business aviation Beijing",
            "ultra long range jets",
            "VIP terminal Beijing",
            "Beijing Hong Kong private jet"
        ]
        
        comparison = analyzer.get_trend_data(top_5_keywords, timeframe='today 12-m')
        
        if not comparison.empty:
            print("\n过去12个月平均热度对比:")
            for kw in top_5_keywords:
                if kw in comparison.columns:
                    avg = comparison[kw].mean()
                    trend = '📈' if comparison[kw].iloc[-1] > comparison[kw].iloc[0] else '📉'
                    print(f"  {trend} {kw:<40} {avg:.1f}")
        
        print("\n🎉 分析完成! 建议根据热度数据调整关键词优先级")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pytrends()