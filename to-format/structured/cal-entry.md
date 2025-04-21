Reformat the following text into a JSON calendar entry in ICS format.  
- Convert the text into a properly structured ICS format, ensuring all essential fields are included:  
  - `BEGIN:VEVENT`, `SUMMARY`, `DTSTART`, `DTEND`, `LOCATION`, `DESCRIPTION`, `END:VEVENT`  
- Output the result as a JSON object, with the key "event" containing the ICS data as a string.  
- Ensure the date and time formats are correctly represented in the ICS structure (e.g., `DTSTART;TZID=America/New_York:20230421T100000`).
