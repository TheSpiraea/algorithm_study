import shlex

#node 정의
class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = self
        self.next = self

class CircularDoublyLinkedList:
    def __init__(self):
        self.sentinel = Node()  # 센티널 더미 노드

    def is_empty(self):
        return self.sentinel.next is self.sentinel
    
    # 센티널 앞과 뒤를 연결하는 메서드
    def append(self, data):
        new_node = Node(data)
        
        tail = self.sentinel.prev
        
        new_node.prev = tail
        new_node.next = self.sentinel
        
        tail.next = new_node
        self.sentinel.prev = new_node
    
    #맨 앞에 삽입하는 메서드
    def prepend(self, data):
        new_node = Node(data)

        head = self.sentinel.next

        # 센티널과 head 사이에 node를 추가함
        new_node.prev = self.sentinel
        new_node.next = head

        head.prev = new_node
        self.sentinel.next = new_node
    
    #순회시 센티널을 만나면 종료하도록 하는 메서드 
    def to_list(self):
        result = []
        cur = self.sentinel.next  # head
        while cur is not self.sentinel:
            result.append(cur.data)
            cur = cur.next
        return result
    
    def to_list_reverse(self):
        result = []
        cur = self.sentinel.prev  # tail
        while cur is not self.sentinel:
            result.append(cur.data)
            cur = cur.prev
        return result

    
    # 앞을 삭제하는 메서드
    def pop_front(self):
        if self.is_empty():
            return None

        node = self.sentinel.next 
        next_node = node.next
        
        #sentinel <-> next_node로 이어붙이기
        self.sentinel.next = next_node
        next_node.prev = self.sentinel
        return node.data
        
    #뒤를 삭제하는 메서드
    def pop_back(self):
        if self.is_empty():
            return None

        node = self.sentinel.prev 
        prev_node = node.prev
        
        prev_node.next = self.sentinel
        self.sentinel.prev = prev_node
        
        return node.data
    
    def find(self, data):
        cur = self.sentinel.next
        while cur is not self.sentinel:
            if cur.data == data:
                return cur
            cur = cur.next
        return None
    
    def contains(self, data):
        return self.find(data) is not None
    
    def remove(self, data):
        node = self.find(data)
        if node is None: 
            return False
        
        node.prev.next = node.next
        node.next.prev = node.prev
        return True
    
    #중간 삽입하는 메서드
    def insert_after(self, target_data, new_data):
        target = self.find(target_data)
        if target is None:
            return False

        new_node = Node(new_data)
        next_node = target.next

        new_node.prev = target
        new_node.next = next_node

        target.next = new_node
        next_node.prev = new_node

        return True
 
HELP = """Commands (원형 이중 연결 리스트):
  append <n...>          : 맨 뒤(tail)에 값 추가 (여러 개 가능)
  prepend <n...>         : 맨 앞(head)에 값 추가 (여러 개 가능)
  insert_after <t> <n>   : 값 t 뒤에 값 n 삽입
  remove <n>             : 값이 n인 노드(처음 발견한 1개) 삭제
  pop_front              : 맨 앞(head) 삭제 후 값 출력
  pop_back               : 맨 뒤(tail) 삭제 후 값 출력
  find <n>               : 값 n 존재 여부 True/False 출력
  show                   : 정방향 리스트 출력
  showrev                : 역방향 리스트 출력
  empty                  : 비어있는지 True/False 출력
  clear                  : 리스트 초기화(비우기)
  help                   : 도움말 출력
  quit / exit            : 종료

Examples:
  append 10 20 30
  prepend 5
  insert_after 20 25
  show
"""

def _parse_ints(parts):
    try:
        return [int(x) for x in parts]
    except ValueError:
        raise ValueError("인자는 모두 정수여야 합니다.")

def repl():
    cll = CircularDoublyLinkedList()
    print("CircularDoublyLinkedList CLI. type 'help'.")

    while True:
        try:
            line = input("cdll> ").strip()
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
                    cll.append(n)
                print(cll.to_list())

            elif cmd == "prepend":
                nums = _parse_ints(args)
                # prepend 1 2 3 => [1,2,3,...] 되게 역순으로 prepend
                for n in reversed(nums):
                    cll.prepend(n)
                print(cll.to_list())

            elif cmd == "insert_after":
                if len(args) != 2:
                    print("usage: insert_after <target> <new>")
                    continue
                t, n = _parse_ints(args)
                ok = cll.insert_after(t, n)
                print(("OK" if ok else "NOT FOUND"), cll.to_list())

            elif cmd == "remove":
                if len(args) != 1:
                    print("usage: remove <n>")
                    continue
                (n,) = _parse_ints(args)
                ok = cll.remove(n)
                print(("OK" if ok else "NOT FOUND"), cll.to_list())

            elif cmd == "pop_front":
                v = cll.pop_front()
                print(v, cll.to_list())

            elif cmd == "pop_back":
                v = cll.pop_back()
                print(v, cll.to_list())

            elif cmd == "find":
                if len(args) != 1:
                    print("usage: find <n>")
                    continue
                (n,) = _parse_ints(args)
                print(cll.contains(n))

            elif cmd == "show":
                print(cll.to_list())

            elif cmd == "showrev":
                print(cll.to_list_reverse())

            elif cmd == "empty":
                print(cll.is_empty())

            elif cmd == "clear":
                cll = CircularDoublyLinkedList()
                print("cleared")

            else:
                print("unknown command. type 'help'.")

        except Exception as e:
            print("error:", e)

if __name__ == "__main__":
    repl()
