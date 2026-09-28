<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>To-Do & D-Day</title>
  <style>
    body { font-family: sans-serif; max-width: 500px; margin: 30px auto; padding: 20px; }
    section { border: 1px solid #ccc; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    ul { list-style: none; padding: 0; }
    li { display: flex; justify-content: space-between; margin-bottom: 8px; }
  </style>
</head>
<body>

  <!-- D-Day 계산기 -->
  <section>
    <h2>D-Day 계산기</h2>
    <input type="text" id="ddayTitle" placeholder="목표 이름">
    <input type="date" id="ddayDate">
    <button onclick="addDday()">추가</button>
    <ul id="ddayList"></ul>
  </section>

  <!-- To-Do 리스트 -->
  <section>
    <h2>To-Do 리스트</h2>
    <input type="text" id="todoInput" placeholder="할 일 입력">
    <button onclick="addTodo()">추가</button>
    <ul id="todoList"></ul>
  </section>

  <script>
    // D-Day 추가 기능
    function addDday() {
      const title = document.getElementById('ddayTitle').value;
      const dateVal = document.getElementById('ddayDate').value;
      if (!title || !dateVal) return;

      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const targetDate = new Date(dateVal);
      targetDate.setHours(0, 0, 0, 0);

      const diffTime = targetDate - today;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      let ddayText = '';
      if (diffDays === 0) ddayText = 'D-Day';
      else if (diffDays > 0) ddayText = `D-${diffDays}`;
      else ddayText = `D+${Math.abs(diffDays)}`;

      const li = document.createElement('li');
      li.innerHTML = `<span>${title}</span> <strong>${ddayText}</strong>`;
      document.getElementById('ddayList').appendChild(li);

      document.getElementById('ddayTitle').value = '';
      document.getElementById('ddayDate').value = '';
    }

    // To-Do 추가 기능
    function addTodo() {
      const input = document.getElementById('todoInput');
      const text = input.value.trim();
      if (!text) return;

      const li = document.createElement('li');
      li.innerHTML = `<span>${text}</span> <button onclick="this.parentElement.remove()">삭제</button>`;
      document.getElementById('todoList').appendChild(li);

      input.value = '';
    }
  </script>

</body>
</html>
