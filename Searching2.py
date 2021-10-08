# ���� �ʿ��� �Լ��� ���̺귯���� import�Ѵ�.
from bs4 import BeautifulSoup
from requests import get
from re import compile, findall, sub

# Just a function that turns lists into strings because the re.findall() really annoys me
def lststr(lst):
    string = ''
    return string.join(lst)

# �� .py ������ �����ϸ� ����� main method�̴�.
def main():
    # ���� ǥ���� "�Խù� �˻�"���� ��ġ�ϸ� ������ ��� ������ ��ũ�̴�.
    link = input("DCINSIDE ����ǥ�� �˻� ������ ��ũ: ")
    #link = "https://search.dcinside.com/post/q/.ED.96.89.EB.B3.B5"
    
    """�˻� ����Ʈ ����(�˻� Ű���� : ������) :
    ���� ���������� �ٷ� ������ Ű���带 �˻����� �� ������ �ּ�
    https://www.ppomppu.co.kr/search_bbs.php?keyword=%B0%AD%BE%C6%C1%F6
    """
    
    i = 1
    """��� �������� �˻� ����� ��ũ�� return �ϴµ� �˻Ѵ� �Խñ� ���� õ ������ �ѱ淡...
    �ʹ� ������ ������ while(1)�� while(i < 500) ������ �ٲټ���
    �׷� 500������������ ��ũ�� ����մϴ�.
    �̰͵� �ʹ� ������ 100���� �ٲ㵵 �˴ϴ�."""
    while(1):
        link = link + "&bbs_cate=2&search_type=sub_memo&order_typedate&page_no="+str(i)

    #�� �������� html�� text�� �����´�.
        html_text = get(link).text

    # �� html ������ �� �� �ٷ�� ���� BeautifulSoup�� �����.
        soup = BeautifulSoup(html_text, 'lxml')
    
        span_list = soup.findAll('span', class_ = 'title')
        
        if not span_list:
            break

    # �� �ȿ��� ��ũ�� �� ������ �ͱ� ������ regular expression(���� ǥ��)�� ����Ѵ�.
        r = compile('href="(.*?)"')
    # for loop�� ���� ����� ����Ʈ
        url_list = []

        for link2 in span_list:
        
        # re library�� string�� input���� �޾ƾ��ϱ� ������ str()�� ����Ѵ�.
            link2 = str(link2)
        # re library�� ����� ��ũ �κи� ���´�. �׷��� findall()�� list�� return�Ѵ�. ��������!!!
            url = r.findall(link2)
        # �׷��� �Ʊ� ������ �Լ��� ����Ѵ� ��
            url_str = lststr(url)
        #����� ����Ʈ�� �߰����ش�.
            url_list.append(url_str)

    #�ٸ� ����Ʈ������ �̷� ������ �߻��ϴ� ���� �𸣰�����, "&"�� "&amp;"�� �ٲ�� ���������� ������ �Ͼ��.
    #�װ͵� ��������. �� �׷��� ��ũ�� �����̴�.
        new_list = []
    #��ũ���� �������� �κе��� �����ش�.
        for url in url_list:
            url = "https://www.ppomppu.co.kr"+url
            new_list.append(sub('&amp;', "&", url))

    # ����� ��� �� �ƴ� �� Ȯ���ϴ� for loop.
        for url in new_list:
            print(url)
        i += 1

    #url���� txt���Ͽ� �����Ѵ�.
        with open("url_list.txt", "w") as f:
            for url in new_list:
                f.write(url + "\n")
#�� �ĸ��� �����ϸ� main method�� �����ϵ��� �Ѵ�.
if __name__ == "__main__":
    main()