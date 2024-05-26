// ======= code for checkbox ======

document.addEventListener('DOMContentLoaded', function () {
    const cbSelectAll = document.getElementById('cbSelectAll');
    const cbRows = document.querySelectorAll('.cbRow');
    const statusCells = document.querySelectorAll('.student_data tbody .status');


    cbSelectAll.addEventListener('change', function () {
        cbRows.forEach(function (cbRow) {
            cbRow.checked = cbSelectAll.checked;
            updateStatus(cbRow);
        });
    });

    cbRows.forEach(function (cbRow) {
        cbRow.addEventListener('change', function () {
            const allChecked = Array.from(cbRows).every(function (cb) {
                return cb.checked;
            });
            const allUnchecked = Array.from(cbRows).every(function (cb) {
                return !cb.checked;
            });

            cbSelectAll.checked = allChecked;
            cbSelectAll.indeterminate = !(allChecked || allUnchecked);
            updateStatus(cbRow);
        });
    });
    
// ====== function to update status when checkbox is checked or unchecked =======

    function updateStatus(checkbox) {
        const row = checkbox.closest('tr');
        const statusCell = row.querySelector('.status');
        if (checkbox.checked) {
          statusCell.textContent = 'P';
        } else {
          statusCell.textContent = 'A';
        }
      }


// ====== code for period select dropdown ========

    const periodSelect = document.getElementById('periodSelect');
    const periodCells = document.querySelectorAll('.student_data tbody .period');
  
    // Set the default value in the period cells
    const defaultPeriod = periodSelect.options[0].value;
    periodCells.forEach(function(cell) {
      cell.textContent = defaultPeriod;
    });
  
    periodSelect.addEventListener('change', function() {
      const selectedPeriod = periodSelect.value;
      periodCells.forEach(function(cell) {
        cell.textContent = selectedPeriod;
      });
    });


// ======= code for displaying confirm & alert prompt =========
  const submitBtn = document.getElementById('submitBtn');
  const periodInput = document.getElementById('periodInput');
  const teacherDateInput = document.getElementById('teacherDateInput');
  
  submitBtn.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission
    const selectedPeriod = periodSelect.value;
    if (selectedPeriod === '--') {
      alert('Please select the period before submitting.');
      return; // Exit the   function if the period is not selected
    }
    const confirmSubmission = confirm('Responses cannot be changed after submission. Are you sure you want to submit?');


// ===== code for storing registration number, attendance status along with systems date =======
    if (confirmSubmission) {
      periodInput.value = selectedPeriod; // set the selected period value in the hidden input field
      teacherDateInput.value = new Date().toISOString(); // storing the teacher's system date in the hidden input field

      const attendanceData = Array.from(cbRows).map(cbRow => {
        return {
          registration_no: cbRow.value,
          attendance_status: cbRow.checked ? 'P' : 'A'
        };
      });

// ======code to send all the data =========
const attendanceDataTextarea = document.getElementById('attendanceDataTextarea');
attendanceDataTextarea.value = JSON.stringify(attendanceData);

const form = document.getElementById('attendanceForm');
form.submit();   
    }
  });
});