\# IPL Data Quality Log



| Table | Column / Area | Data Quality Issue | Evidence / Finding | Cleaning Decision |

|---|---|---|---|---|

| matches | city | Missing values | 51 NULL values | Use venue city first, then match city, then UNKNOWN |

| matches | match\_number | Missing values | 70 NULL values | Keep as missing; do not invent values |

| matches | player\_of\_match | Empty strings | 9 empty values | Treat empty strings as missing |

| matches | win\_by\_runs | NULL values | 666 NULL values | Keep as NULL where not applicable |

| matches | win\_by\_wickets | NULL values | 571 NULL values | Keep as NULL where not applicable |

| matches | venue | Fragmented venue names | 59 distinct raw names; comma rule reduces to 42 | Normalize text before venue analysis |

| matches | venue | Remaining punctuation variant | M Chinnaswamy Stadium and M.Chinnaswamy Stadium represent the same venue | Apply second-pass rule; final distinct venues = 41 |

| matches | season | Mixed season format | Includes value such as 2020/21 | Take first four characters before CAST to INTEGER |

| deliveries | bowler\_type | Whitespace-only values | 8 whitespace-only values | TRIM and convert blank values to NULL |

| deliveries | bowler\_type | Capitalisation variant | Same bowling style appears with different capitalisation | Standardize with CASE WHEN |

| players | field\_pos | Missing / blank values | 88 NULL + 612 blank values = 700 | TRIM and convert blanks to NULL |

| venues | venue | Duplicate rows | 63 rows but 59 distinct venue names | Keep first row per venue using ROW\_NUMBER |

