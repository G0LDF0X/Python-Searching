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
    tmp_link = link
    # link = "https://search.dcinside.com/post/q/.ED.96.89.EB.B3.B5"
    """�������� ������ ��ũ :
        https://search.dcinside.com/post/p/1/q/.ED.96.89.EB.B3.B5
    """
    
    """������ ���� ������ �ƴ��� ���ϱ� ���� �ӽ� string ����"""
    tmp_str = ''
    
    """�ӽ÷� �ִ� 200���������� ������� �� �÷��� OK. �Ʒ� tmp_link�� �Է��� ��ũ �߰��� ������ ���� ��������"""
    for i in range(1, 200):
        tmp_link = link[:32]+"/p/"+str(i)+"/"+link[33:]

    #�� �������� html�� text�� �����´�.
        html_text = get(tmp_link).text

    # �� html ������ �� �� �ٷ�� ���� BeautifulSoup�� �����.
        soup = BeautifulSoup(html_text, 'lxml')
    # ���ϴ� url���� �ִ� class�� ã�´�.
        sch_list= soup.find_all('a', class_= 'tit_txt')
    # �� �ȿ��� ��ũ�� �� ������ �ͱ� ������ regular expression(���� ǥ��)�� ����Ѵ�.
        r = compile('href="(.*?)"')
    # for loop�� ���� ����� ����Ʈ
        url_list = []

        for link2 in sch_list:
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
            new_list.append(sub('&amp;', "&", url))
        
        """���� �������� ù ��° �ּҿ� ���� �������� ù��° �ּҰ� �����ϸ� �� �̻� �������� ���� ������ �����ϰ� for���� ��������"""
        if(tmp_str == new_list[0]):
            break
        else:    
            tmp_str = new_list[0]

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