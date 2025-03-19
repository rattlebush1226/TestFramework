// TestFramework/static/js/date_to_timestamp.js

document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('id_date_input');
    const timestampOutput = document.getElementById('id_timestamp_output');

    if (dateInput && timestampOutput) {
        const generateButton = document.createElement('button');
        generateButton.textContent = '生成时间戳';
        generateButton.id = 'generate_timestamp_button';

        // 将按钮插入到日期输入框后面
        dateInput.parentNode.insertBefore(generateButton, dateInput.nextSibling);

        generateButton.addEventListener('click', function () {
            const date = new Date(dateInput.value);
            const timestamp = date.getTime();
            if (!isNaN(timestamp)) {
                timestampOutput.value = timestamp;
            } else {
                timestampOutput.value = '无效日期';
            }
        });
    }
});