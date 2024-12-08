document.addEventListener("DOMContentLoaded", function () {
    const selectElement = document.querySelector('.select-calculators-container__select');

    const selectElement2 = document.getElementById('download-select');
    if (selectElement2) {
        const options = selectElement2.querySelectorAll('option');
        options.forEach(option => {
            option.style.color = 'orange';
        });
    }

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

    const collectAndSendData = (isFactCalculation = false) => {
        const errorContainer = document.getElementById('error-container');
        errorContainer.innerHTML = '';

        const requiredFields = {
            'fact_avg_fails_month_day': 'День факт среднее кол-во файлов в месяц',
            'fact_avg_fails_month_day_weekends': 'Ночь/пр/вых факт среднее кол-во файлов в месяц',
            'fact_avg_fails_month_night_weekends': 'День/пр/вых факт среднее кол-во файлов в месяц',
            'fact_machine_count_180': 'Факт кол-во машин 180 часов',
            'fact_machine_count_168': 'Факт кол-во машин 168 часов',
            'fact_machine_count_79': 'Факт кол-во машин 79 часов'
        };

        let hasErrors = false;
        const inputData = {};

        // Проверяем каждое поле
        for (const [fieldName, fieldLabel] of Object.entries(requiredFields)) {
            const input = document.querySelector(`[name="${fieldName}"]`);
            const value = input.value.trim();
            
            if (!value) {
                hasErrors = true;
                input.style.borderColor = 'red';
            } else {
                input.style.borderColor = '';
                inputData[fieldLabel] = parseInt(value) || 0;
            }
        }

        // Проверка поля новых пользователей только для плановых расчетов
        const newUsersInput = document.querySelector('[name="new_users"]');
        if (!isFactCalculation) {
            const newUsersValue = parseInt(newUsersInput.value) || 0;
            
            if (!newUsersInput.value.trim() || newUsersValue === 0) {
                hasErrors = true;
                newUsersInput.style.borderColor = 'red';
            } else {
                newUsersInput.style.borderColor = '';
                inputData['Общее кол-во новых пользователей (УЗ)'] = newUsersValue;
            }
        } else {
            // Для фактических расчетов всегда передаем 0
            inputData['Общее кол-во новых пользователей (УЗ)'] = 0;
            newUsersInput.style.borderColor = '';
        }

        if (hasErrors) {
            errorContainer.innerHTML = `
                <div class="error-message" style="color: red; text-align: center;">
                    Пожалуйста, заполните все обязательные поля
                </div>
            `;
            return null;
        }

        return inputData;
    };

    factBtn.addEventListener('click', () => {
        const data = collectAndSendData(true);
        if (!data) return;

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

            console.log('Новый HTML:', data.html_content);
            resultsContainer.innerHTML = data.html_content;
        })
        .catch(error => {
            console.error('Ошибка при отправке данных:', error);
        });
    });

    planBtn.addEventListener('click', () => {
        const data = collectAndSendData(false);
        if (!data) return;

        const newUsersInput = document.querySelector('[name="new_users"]');
        const errorContainer = document.getElementById('error-container');
        
        // Дополнительная проверка поля новых пользователей
        if (!newUsersInput.value.trim()) {
            // Возвращаем красные границы всем пустым обязательным полям
            const requiredFields = {
                'fact_avg_fails_month_day': 'День факт среднее кол-во файлов в месяц',
                'fact_avg_fails_month_day_weekends': 'Ночь/пр/вых факт среднее кол-во файлов в месяц',
                'fact_avg_fails_month_night_weekends': 'День/пр/вых факт среднее кол-во файлов в месяц',
                'fact_machine_count_180': 'Факт кол-во машин 180 часов',
                'fact_machine_count_168': 'Факт кол-во машин 168 часов',
                'fact_machine_count_79': 'Факт кол-во машин 79 часов'
            };

            for (const fieldName of Object.keys(requiredFields)) {
                const input = document.querySelector(`[name="${fieldName}"]`);
                if (!input.value.trim()) {
                    input.style.borderColor = 'red';
                }
            }

            newUsersInput.style.borderColor = 'red';
            errorContainer.innerHTML = `
                <div class="error-message" style="color: red; text-align: center;">
                    Пожалуйста, заполните все обязательные поля
                </div>
            `;
            return;
        }

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

            console.log('Новый HTML:', data.html_content);
            resultsContainer.innerHTML = data.html_content;
        })
        .catch(error => {
            console.error('Ошибка при отправке данных:', error);
        });
    });

    downloadSelect.addEventListener('change', function() {
        const selectedFormat = this.value;
        if (selectedFormat) {
            const data = collectAndSendData(true);
            if (!data) return;

            console.log('Отправляемые данные:', data);
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

    // Обновляем обработчик для очистки ошибок при вводе
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('input', function() {
            this.style.borderColor = '';
        });
    });
});