document.addEventListener('DOMContentLoaded', function() {
    const generateButton = document.getElementById('generate-timestamp-button');
    const dateInput = document.getElementById('date-input'); // 假设日期输入框的 id 为 date-input
    const timestampOutput = document.getElementById('timestamp-output'); // 假设时间戳输出框的 id 为 timestamp-output

    generateButton.addEventListener('click', function() {
        const dateValue = dateInput.value;
        const timestamp = new Date(dateValue).getTime();
        if (!isNaN(timestamp)) {
            timestampOutput.value = timestamp;
        } else {
            timestampOutput.value = '无效日期';
        }
    });
});