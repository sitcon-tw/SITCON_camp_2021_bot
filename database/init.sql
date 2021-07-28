CREATE TABLE IF NOT EXISTS `point_code` (
  code TEXT PRIMARY KEY,
  point INT NOT NULL,
  used_by INT DEFAULT 0 -- group id, i.e. 1-10, -1 for deleted
);
