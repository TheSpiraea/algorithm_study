import shlex


# double_linked_list node 정의
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    # double linked list에 노드를 추가하는 메서드
    def append(self, data):
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
     
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
        
    # double linked list 맨 앞 추가하는 기능
    def prepend(self, data):
        new_node = Node(data)
        
        # 비어있으면 첫 노드로 간주
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
        
        # 헤드를 새로운 노드에게 붙여줌
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node
    
    # 값으로 노드를 하나 찾아서 삭제하는 메서드
    def remove(self, data):
        cur = self.head
        
        #삭제할 노드를 찾기
        while cur is not None and cur.data != data:
            cur = cur.next
        #노드 못찾은 경우
        if cur is None:
            return False
        #노드 찾음, 연결을 끊고서 이어 붙이기
        if cur.prev is None:          # head 삭제
            self.head = cur.next
        else:
            cur.prev.next = cur.next

        if cur.next is None:          # tail 삭제
            self.tail = cur.prev
        else:
            cur.next.prev = cur.prev
        return True

    # double linked list 출력하는 기능
    def print_forward(self):
        cur = self.head
        while cur is not None:
            print(cur.data, end=" ")
            cur = cur.next
        print()

    def print_backward(self):
        cur = self.tail
        while cur is not None:
            print(cur.data, end=" ")
            cur = cur.prev
        print()

    #검색기능, 값으로 노드를 찾아서 노드 자체를 반환하거나, 노드가 있는지 없는지만 확인하는기능
    def find(self, data):
        cur = self.head
        while cur is not None:
            if cur.data == data:
                return cur
            cur = cur.next 
        return None
    
    def contains(self, data):
        return self.find(data) is not None
    
    
    # node의 리스트를 확인하는 메서드
    def to_list(self):
        result = []
        cur = self.head
        while cur is not None:
            result.append(cur.data)
            cur = cur.next
        return result
    
    # node의 리스트를 역순으로 확인하는 메서드
    def to_list_reverse(self):
        result = []
        cur = self.tail
        while cur is not None:
            result.append(cur.data)
            cur = cur.prev
        return result

    # 중간에 node를 삽입하는 메서드
    def insert_after(self, target_data, new_data):
        cur = self.head
        
        while cur is not None and cur.data != target_data:
            cur = cur.next
        
        if cur is None:
            return False
        
        new_node = Node(new_data)

        new_node.prev = cur
        new_node.next = cur.next
        
        if cur.next is None:
            self.tail = new_node
        else:
            cur.next.prev = new_node
        
        cur.next = new_node
        return True
    
    #앞 삽입
    def pop_front(self):
        if self.head is None:
            return None

        node = self.head
        self.head = self.head.next
        
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        return node.data
    

    #뒤 삽입
    def pop_back(self):
        if self.tail is None:
            return None
        
        node = self.tail
        self.tail = node.prev
        
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
            
        return node.data

# 인터페이스 -> 이부분은 gpt 사용
HELP = """
  Commands (명령어):
  append <n...>          : 리스트 맨 뒤(tail)에 값 추가 (여러 개 가능)
  prepend <n...>         : 리스트 맨 앞(head)에 값 추가 (여러 개 가능)
  insert_after <t> <n>   : 값 t를 가진 노드 “뒤에” 값 n 삽입
  remove <n>             : 값이 n인 노드(처음 발견한 1개) 삭제
  pop_front              : 맨 앞(head) 노드 삭제 후 그 값 출력/반환
  pop_back               : 맨 뒤(tail) 노드 삭제 후 그 값 출력/반환
  find <n>               : 값 n이 존재하는지 True/False 출력
  show                   : 리스트를 정방향(head → tail)으로 출력
  showrev                : 리스트를 역방향(tail → head)으로 출력
  clear                  : 리스트 초기화(비우기)
  help                   : 도움말(이 목록) 출력
  quit / exit            : 종료

Examples (예시):
  append 10 20 30
  prepend 5
  insert_after 20 25
  show
"""

def _parse_ints(parts):
    try:
        return [int(x) for x in parts]
    except ValueError:
        raise ValueError("All arguments must be integers.")

def repl():
    dll = DoubleLinkedList()
    print("DoubleLinkedList CLI. type 'help'.")

    while True:
        try:
            line = input("dll> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue

        try:
            parts = shlex.split(line)
        except ValueError as e:
            print("parse error:", e)
            continue

        cmd = parts[0].lower()
        args = parts[1:]

        try:
            if cmd in ("quit", "exit"):
                break

            elif cmd == "help":
                print(HELP)

            elif cmd == "append":
                nums = _parse_ints(args)
                for n in nums:
                    dll.append(n)
                print(dll.to_list())

            elif cmd == "prepend":
                nums = _parse_ints(args)
                for n in reversed(nums):
                    dll.prepend(n)
                print(dll.to_list())

            elif cmd == "insert_after":
                if len(args) != 2:
                    print("usage: insert_after <target> <new>")
                    continue
                t, n = _parse_ints(args)
                ok = dll.insert_after(t, n)
                print(("OK" if ok else "NOT FOUND"), dll.to_list())

            elif cmd == "remove":
                if len(args) != 1:
                    print("usage: remove <n>")
                    continue
                (n,) = _parse_ints(args)
                ok = dll.remove(n)
                print(("OK" if ok else "NOT FOUND"), dll.to_list())

            elif cmd == "pop_front":
                v = dll.pop_front()
                print(v, dll.to_list())

            elif cmd == "pop_back":
                v = dll.pop_back()
                print(v, dll.to_list())

            elif cmd == "find":
                if len(args) != 1:
                    print("usage: find <n>")
                    continue
                (n,) = _parse_ints(args)
                print(dll.contains(n))

            elif cmd == "show":
                print(dll.to_list())

            elif cmd == "showrev":
                print(dll.to_list_reverse())

            elif cmd == "clear":
                dll = DoubleLinkedList()
                print("cleared")

            else:
                print("unknown command. type 'help'.")

        except Exception as e:
            print("error:", e)

if __name__ == "__main__":
    repl()