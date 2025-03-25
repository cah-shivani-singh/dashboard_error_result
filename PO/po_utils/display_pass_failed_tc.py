import matplotlib.pyplot as plt
import sys
sys.path.append('PO')
import base64

def display_pi_chart_for_tc(total_tc, pass_tc, failed_tc, folder_path):
    '''
    this will create a pi chart with failed and pass tc
    '''
    total_testcases = total_tc
    passed_test_cases = pass_tc
    failed_test_cases = failed_tc
    labels = ['Passed','Failed']
    sizes=[passed_test_cases,failed_test_cases]
    colors = ['#4CAF50','#F44336']

    plt.pie(sizes,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=140)
    plt.axis('equal')
    plt.title('Test Case Result')
    plt.savefig(f'{folder_path}\pie_chart.png')


