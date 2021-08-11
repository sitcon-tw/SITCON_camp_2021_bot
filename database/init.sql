CREATE TABLE IF NOT EXISTS `point_code` (
  code TEXT PRIMARY KEY,
  point INT NOT NULL,
  used_by INT DEFAULT 0, -- group id, i.e. 1-10, -1 for deleted
  used_at DATETIME
);

CREATE TABLE IF NOT EXISTS `message` (
  id INT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `submissions` (
  id INTEGER PRIMARY KEY,
  group_id INT NOT NULL,
  task_id TEXT NOT NULL,
  password TEXT NOT NULL,
  is_correct INT NOT NULL,
  submitted_at DATETIME DEFAULT (DATETIME('now', 'localtime'))
);
