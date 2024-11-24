document.addEventListener("DOMContentLoaded", function () {
    const selectElement = document.querySelector('.select-calculators-container__select');

    if (!selectElement) {
        console.error("Select element not found!");
        return;
    }

    selectElement.addEventListener('change', function () {
        const selectedValue = selectElement.value;
        if (!selectedValue) return;

        window.location.href = `/calculator/${selectedValue}`;
    });

    const currentPath = window.location.pathname;
    const calculatorId = currentPath.split('/')[2];

    if (calculatorId) {
        selectElement.value = calculatorId;
    }

    const factBtn = document.querySelector('.fact-btn');
    const planBtn = document.querySelector('.plan-btn');
    const downloadSelect = document.querySelector('.download-btn');

    if (!factBtn || !planBtn || !downloadSelect) {
        console.error("Calculation buttons or download select not found!");
        return;
    }

    const collectAndSendData = () => {
        const inputData = {
            'День факт среднее кол-во файлов в месяц': document.querySelector('[name="fact_avg_fails_month_day"]').value || 0,
            'Ночь/пр/вых факт среднее кол-во файлов в месяц': document.querySelector('[name="fact_avg_fails_month_day_weekends"]').value || 0,
            'День/пр/вых факт среднее кол-во файлов в месяц': document.querySelector('[name="fact_avg_fails_month_night_weekends"]').value || 0,
            'Общее кол-во новых пользователей (УЗ)': document.querySelector('[name="new_users"]').value || 0,
            'Факт кол-во машин 180 часов': document.querySelector('[name="fact_machine_count_180"]').value || 0,
            'Факт кол-во машин 168 часов': document.querySelector('[name="fact_machine_count_168"]').value || 0,
            'Факт кол-во машин 79 часов': document.querySelector('[name="fact_machine_count_79"]').value || 0,
        };

        console.log('Собранные данные:', inputData);

        return inputData;
    };

    factBtn.addEventListener('click', () => {
        const data = collectAndSendData();
        fetch('/calculate-fact/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            console.log('Raw response:', response);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Ответ сервера:', data);

            const resultsContainer = document.getElementById('results-container');
            if (!resultsContainer) {
                console.error("Results container not found!");
                return;
            }

            console.log('Новый HTML:', data.html_content); // Логирование нового HTML содержимого

            resultsContainer.innerHTML = data.html_content; // Обновляем HTML-содержимое страницы
        })
        .catch(error => {
            console.error('Ошибка при отправке данных:', error);
        });
    });

    planBtn.addEventListener('click', () => {
        const data = collectAndSendData();
        fetch('/calculate-plan/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            console.log('Raw response:', response);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Ответ сервера:', data);

            const resultsContainer = document.getElementById('results-container');
            if (!resultsContainer) {
                console.error("Results container not found!");
                return;
            }

            console.log('Новый HTML:', data.html_content); // Логирование нового HTML содержимого

            resultsContainer.innerHTML = data.html_content; // Обновляем HTML-содержимое страницы
        })
        .catch(error => {
            console.error('Ошибка при отправке данных:', error);
        });
    });

downloadSelect.addEventListener('change', function() {
    const selectedFormat = this.value;
    if (selectedFormat) {
        const data = collectAndSendData();
        console.log('Отправляемые данные:', data); // Логирование отправляемых данных
        fetch(`/export/?format=${selectedFormat}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    console.error(`HTTP error! status: ${response.status}, response: ${text}`);
                    throw new Error(`HTTP error! status: ${response.status}, response: ${text}`);
                });
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `file.${selectedFormat}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Ошибка при отправке данных:', error);
        });
    }
});

});
