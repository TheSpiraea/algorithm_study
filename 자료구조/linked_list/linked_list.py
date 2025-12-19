# node 정의 및 단일 연결 리스트 구현
class Node:
    # node 정의 value : 저장할 데이터, next : 다음 노드를 가리키는 링크
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    # 인스턴스로 노드 복제 (현재 노드의 value를 복사한 새 노드를 만든다.)
    def clone(self):
        return Node(self.value)
    
    

# 단일 연결 리스트 클래스 정의
class SinglyLinkedList:
    def __init__(self):
        self.head = None

   # 헤드를 연결하는 메서드
    def set_head(self, node):
        self.head = node

    # 노드를 탐색하는 메서드
    def find(self, value):
        
        # value를 가진 첫 노드를 찾아 반환한다.
        cur = self.head
        while cur is not None:
            if cur.value == value:
                return cur
            cur = cur.next
        return None

    # 인덱스로 노드를 가져오는 메서드
    def get(self, index):
        cur = self.head
        i = 0
        while cur is not None:
            if i == index:
                return cur
            cur = cur.next
            i += 1
        return None

    # 맨 앞에 삽입하는 메서드
    def push_front(self, value):
        """
        새 노드를 맨 앞(head)에 삽입한다.
        """
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        return new_node

    #맨 앞을 삭제하는 메서드
    def pop_front(self):
        """
        맨 앞 노드를 제거하고 그 value를 반환한다.
        비어있으면 None 반환.
        """
        if self.head is None:
            return None
        removed = self.head
        self.head = self.head.next
        removed.next = None  # 연결 끊기
        return removed.value

    # 맨 뒤에 삽입하는 메서드
    def push_back(self, value):
        new_node = Node(value)

        # 리스트가 비어있으면 head가 곧 새 노드
        if self.head is None:
            self.head = new_node
            return new_node

        # 끝까지 이동해서 마지막 노드 next에 연결
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node
        return new_node

    # 중간에 삽입하는 메서드
    def insert_after(self, target_value, new_value):
        # target_value를 갖고있는 첫 노드를 찾아서 그 뒤에 new_value를 삽입
        target = self.find(target_value)
        if target is None:
            return False

        new_node = Node(new_value)
        new_node.next = target.next
        target.next = new_node
        return True

    #index 위치에 새 노드를 삽입하는 메서드 (index가 리스트 길이보다 크면 실패)
    def insert_at(self, index, value):
        if index == 0:
            self.push_front(value)
            return True

        prev = self.get(index - 1)  # index 바로 앞 노드
        if prev is None:
            return False  # 삽입 위치가 범위를 벗어남

        new_node = Node(value)
        new_node.next = prev.next
        prev.next = new_node
        return True

    #삭제 기능 메서드
    def delete_value(self, value):
        # head가 삭제 대상이면 pop_front로 처리
        if self.head is None:
            return False
        if self.head.value == value:
            self.pop_front()
            return True

        # 이전(prev)과 현재(cur) 포인터로 탐색
        prev = self.head
        cur = self.head.next

        while cur is not None:
            if cur.value == value:
                prev.next = cur.next
                cur.next = None  # 연결 끊기
                return True
            prev = cur
            cur = cur.next

        return False

    # index 위치의 노드를 삭제하는 메서드
    def delete_at(self, index):
        if self.head is None:
            return None

        # index 0이면 맨 앞 삭제
        if index == 0:
            return self.pop_front()

        prev = self.get(index - 1)
        if prev is None or prev.next is None:
            return None

        removed = prev.next
        prev.next = removed.next
        removed.next = None
        return removed.value

    #리스트를 파이썬 리스트로 변환
    def to_list(self):
        """
        연결 리스트의 값을 [..] 형태로 만들어 반환한다.
        """
        result = []
        cur = self.head
        while cur is not None:
            result.append(cur.value)
            cur = cur.next
        return result


# 인터페이스
if __name__ == "__main__":
    sll = SinglyLinkedList()

    print("=== Singly Linked List 터미널 인터페이스 ===")
    print("명령어:")
    print(" push_front <값>")
    print(" push_back <값>")
    print(" pop_front")
    print(" insert_after <기존값> <새값>")
    print(" insert_at <인덱스> <값>")
    print(" delete_value <값>")
    print(" delete_at <인덱스>")
    print(" find <값>")
    print(" get <인덱스>")
    print(" show")
    print(" exit")

    while True:
        cmd = input(">> ").strip()
        if not cmd:
            continue

        parts = cmd.split()

        if parts[0] == "exit":
            break

        elif parts[0] == "push_front":
            sll.push_front(int(parts[1]))

        elif parts[0] == "push_back":
            sll.push_back(int(parts[1]))

        elif parts[0] == "pop_front":
            print("removed:", sll.pop_front())

        elif parts[0] == "insert_after":
            ok = sll.insert_after(int(parts[1]), int(parts[2]))
            print("success" if ok else "fail")

        elif parts[0] == "insert_at":
            ok = sll.insert_at(int(parts[1]), int(parts[2]))
            print("success" if ok else "fail")

        elif parts[0] == "delete_value":
            ok = sll.delete_value(int(parts[1]))
            print("success" if ok else "fail")

        elif parts[0] == "delete_at":
            print("removed:", sll.delete_at(int(parts[1])))

        elif parts[0] == "find":
            node = sll.find(int(parts[1]))
            print("found" if node else "not found")

        elif parts[0] == "get":
            node = sll.get(int(parts[1]))
            print(node.value if node else None)

        elif parts[0] == "show":
            print(sll.to_list())

        else:
            print("unknown command")
