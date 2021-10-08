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
    
    """�����ŴϾ� ����(�˻� Ű���� : ���) :
    https://cafe.daum.net/_c21_/cafesearch?grpid=10akR&item=subject&sorttype=0&query=%ED%8E%98%EB%AF%B8#"""

    #�� �������� html�� text�� �����´�.
    html_text = get(link).text

    # �� html ������ �� �� �ٷ�� ���� BeautifulSoup�� �����.
    soup = BeautifulSoup(html_text, 'lxml')
    
    """ ���� ���(���� �ڵ�):

    # ���ϴ� url���� �ִ� class�� ã�´�.
    sch_list= soup.find_all('a', class_= 'tit_txt')

    ���λ��̵��� ��� 'tit.txt' �±װ� �������� �ٸ� ���� ������ �ʴ´�.
    
    �����ŴϾ��� ��� html �ڵ带 ���� <tr class='list_row_info'> �ȿ��� �ٽ� �� �� td �±׷� ����, �ű⼭ a �±׸� ������ ��
    ���Ĵ� �𾾿��� �ߴ� �Ͱ� �����ϰ� ���Խ����� href �±׿��� ū����ǥ ���� ��ũ�� �����Ѵ�.
    ��ü���� ������ div id 'container' -> div id 'content' -> div class 'primary content' -> table 'class roundTable'
    -> tbody class 'pos_rel' -> form id 'innerSearchForm' -> table id 'searchCafeList' -> tr class 'list_row_info'��.
    
    BeautifulSoup���� find�� td �±��� id�� class ������ �ٴ� ���� �Ұ����ϱ� ������ (soup.find('td', class_ = 'Ŭ������') �Ұ���)
    ����Ʈ�� index�� �̿��Ͽ� ���ϴ� �κ��� �����Ѵ�.
    """

    """�ټ��� tr �±׿� �˻� ����� ����Ǿ� �ֱ� ������ findAll�� �̿��� ��ü �˻� ����� ����Ʈ�� ��´�."""
    div_list = soup.findAll('tr', class_ = 'list_row_info')
    a_list=[]
    
    for link in div_list:
        tmp_list = link.findAll('td')
        str_tmp = tmp_list[1].find('a')
        a_list.append(str_tmp)
        
    """a_list�� ���� �ڵ��� sch_list�� �����ϴ�. �ش� ����Ʈ�� a �±׸� �����Ѵ�."""

    # �� �ȿ��� ��ũ�� �� ������ �ͱ� ������ regular expression(���� ǥ��)�� ����Ѵ�.
    r = compile('href="(.*?)"')
    # for loop�� ���� ����� ����Ʈ
    url_list = []

    for link in a_list:
        
        # re library�� string�� input���� �޾ƾ��ϱ� ������ str()�� ����Ѵ�.
        link = str(link)
        # re library�� ����� ��ũ �κи� ���´�. �׷��� findall()�� list�� return�Ѵ�. ��������!!!
        url = r.findall(link)
        # �׷��� �Ʊ� ������ �Լ��� ����Ѵ� ��
        url_str = lststr(url)
        #����� ����Ʈ�� �߰����ش�.
        url_list.append(url_str)

    #�ٸ� ����Ʈ������ �̷� ������ �߻��ϴ� ���� �𸣰�����, "&"�� "&amp;"�� �ٲ�� ���������� ������ �Ͼ��.
    #�װ͵� ��������. �� �׷��� ��ũ�� �����̴�.
    new_list = []
    #��ũ���� �������� �κе��� �����ش�.
    for url in url_list:
        """���� �ŴϾƿ��� ������ <a href>�� ��� �պκп� ���� �ּҸ� �ٿ��־�� ��ũ�� ����Ѵ�.
        ����� ī�信 �����ؾ� �˻� ����� �� �� �ֱ� ������ ���� �� ���� üũ�� �����ϴ�."""
        url = "https://cafe.daum.net/"+url
        new_list.append(sub('&amp;', "&", url))

    # ����� ��� �� �ƴ� �� Ȯ���ϴ� for loop.
    for url in new_list:
        print(url)

    #url���� txt���Ͽ� �����Ѵ�.
    with open("url_list.txt", "w") as f:
        for url in new_list:
            f.write(url + "\n")
#�� �ĸ��� �����ϸ� main method�� �����ϵ��� �Ѵ�.
if __name__ == "__main__":
    main()
    
    
"""�⺻������ ��� ���������� ������ ���� �Ǿ� ���� �ʱ� ������ '�������� ��ũ �����'�� �����, 
    ã�ƺ����� �ϴ� �������� �°� �����ϴ� ������ �ʿ��ϴ�.
    
    ���� ���� �ڵ��� ��� 1�������� �˻� ������� �����ֱ� ������(���λ��̵�, �����ŴϾ� �� �� ����) �ٸ� �������� ����� ã�� �ʹٸ�
    for���� �̿��Ͽ� ���� ������ �ݺ��ϸ� �ȴ�. �̶� ���λ��̵��� ��� ������ �ּ��� �߰� �κп�  'p/1/', 'p/2/'���� ���� �־��־��
    �ϸ�, �Ʒ� �ڵ�� �ش� �ݺ� ������ �ݿ��� ��.(�����ŴϾƴ� �˻� ����� 1�������� ���� �ʾƼ� ���λ��̵�� ����.)
"""