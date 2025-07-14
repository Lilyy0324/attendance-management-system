document.getElementById('attendanceForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const attendance = [];
    document.querySelectorAll('select[name="status"]').forEach(select => {
        attendance.push({
            roll_no: select.getAttribute('data-roll'),
            status: select.value
        });
    });

    const res = await fetch('/mark_attendance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ attendance })
    });

    const result = await res.json();
    alert(result.message);
});