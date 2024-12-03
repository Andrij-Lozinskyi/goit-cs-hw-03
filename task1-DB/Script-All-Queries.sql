-- Отримати всі завдання певного користувача
SELECT t.*, s.name as status_name
FROM tasks t
JOIN status s ON t.status_id = s.id
WHERE t.user_id = 1;

-- Вибрати завдання за певним статусом
SELECT t.*, u.fullname
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE t.status_id = (SELECT id FROM status WHERE name = 'new');

-- Оновити статус конкретного завдання
UPDATE tasks 
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;

-- Отримати список користувачів, які не мають жодного завдання
SELECT * 
FROM users 
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);

-- Додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'Нове завдання',
    'Опис завдання',
    (SELECT id FROM status WHERE name = 'new'),
    1
);

-- Отримати всі завдання, які ще не завершено
SELECT t.*, s.name as status_name, u.fullname
FROM tasks t
JOIN status s ON t.status_id = s.id
JOIN users u ON t.user_id = u.id
WHERE s.name != 'completed';

-- Видалити конкретне завдання
DELETE FROM tasks WHERE id = 1;

-- Знайти користувачів з певною електронною поштою
SELECT * 
FROM users 
WHERE email = 'harveymark@example.com';

-- Оновити ім'я користувача
UPDATE users 
SET fullname = 'Нове Ім''я' 
WHERE id = 1;

-- Отримати кількість завдань для кожного статусу
SELECT s.name, COUNT(t.id) as tasks_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name
ORDER BY tasks_count DESC;

-- Отримати завдання користувачів з певним доменом пошти
SELECT t.*, u.fullname, u.email
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com';

-- Отримати список завдань, що не мають опису
SELECT t.*, u.fullname
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE t.description IS NULL OR t.description = '';

-- Вибрати користувачів та їхні завдання у статусі 'in progress'
SELECT u.fullname, t.title, t.description
FROM users u
INNER JOIN tasks t ON u.id = t.user_id
INNER JOIN status s ON t.status_id = s.id
WHERE s.name = 'in progress';

-- Отримати користувачів та кількість їхніх завдань
SELECT u.fullname, u.email, COUNT(t.id) as tasks_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id, u.fullname, u.email
ORDER BY tasks_count DESC;