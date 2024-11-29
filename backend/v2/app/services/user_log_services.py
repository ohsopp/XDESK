import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.image as mpimg
from typing import List
import os

# 로그 데이터를 이용해 그래프를 생성하는 함수
async def logs_to_graph(user_logs: List[dict]):
    if not user_logs:
        return False

    # DataFrame 생성
    df = pd.DataFrame(user_logs)
    
    # log_datetime을 'date'로 변환 (UTC 기준 datetime을 사용)
    df['date'] = pd.to_datetime(df['date'], utc=True)
    
    # 날짜순 정렬 (login_count 제거)
    df = df.sort_values(by='date')
    
    # 그래프 그리기
    plt.figure(figsize=(15, 8))
    plt.plot(df['date'], df['posture_percentage'], linestyle='-', color='darkblue', label='Posture Percentage')
    
    # 최대/최소 포인트 찾기
    max_point = df[df['posture_percentage'] == df['posture_percentage'].max()]
    min_point = df[df['posture_percentage'] == df['posture_percentage'].min()]

    # 날짜와 포인트 값을 적절하게 가져와서 문자열로 변환
    max_date = max_point['date'].dt.strftime('%Y-%m-%d %H:%M:%S').values[0]
    max_value = max_point['posture_percentage'].values[0]
    min_date = min_point['date'].dt.strftime('%Y-%m-%d %H:%M:%S').values[0]
    min_value = min_point['posture_percentage'].values[0]

    # 주석 추가
    plt.gca().annotate(f'Max: {max_value} ({max_date})', xy=(1.01, 0.95), xycoords='axes fraction',
                       fontsize=12, color='green', horizontalalignment='left')
    plt.gca().annotate(f'Min: {min_value} ({min_date})', xy=(1.01, 0.90), xycoords='axes fraction',
                       fontsize=12, color='red', horizontalalignment='left')

    # 첫날과 마지막 날 계산
    start_date = df['date'].min()
    end_date = df['date'].max()

    # 날짜를 10등분하여 생성
    date_ticks = pd.date_range(start=start_date, end=end_date, periods=10)

    # x축 눈금 설정
    plt.xticks(date_ticks, rotation=45)

    # 그래프 설정
    plt.xlabel('Date')
    plt.ylabel('Posture Percentage')
    plt.title(f"User Data Over Time")
    plt.legend()

    file_path = os.path.join(os.getcwd(), 'xdesk.gif')
    if os.path.exists(file_path):
        watermark = mpimg.imread(file_path)
        plt.figimage(watermark, xo=950, yo=50, alpha=0.1, zorder=1)
    else:
        print(f"File not found: {file_path}")
        return plt

    return plt
