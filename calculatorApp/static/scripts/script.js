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
            
            // Специальная проверка для машин 180 часов
            if (fieldName === 'fact_machine_count_180') {
                if (!value || parseInt(value) === 0) {
                    hasErrors = true;
                    input.style.borderColor = 'red';
                    continue;
                }
            }
            
            if (!value) {
                hasErrors = true;
                input.style.borderColor = 'red';
            } else {
                input.style.borderColor = '';
                inputData[fieldLabel] = parseInt(value) || 0;
            }
        }

        // Проверка поля новых пользователей
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
            // Для фактических расчетов берем текущее значение поля, а не устанавливаем 0
            inputData['Общее кол-во новых пользователей (УЗ)'] = parseInt(newUsersInput.value) || 0;
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
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const resultsContainer = document.getElementById('results-container');
            if (!resultsContainer) {
                return;
            }
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
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const resultsContainer = document.getElementById('results-container');
            if (!resultsContainer) {
                return;
            }
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
            if (!data) {
                // Сбрасываем значение select при ошибке незаполненных данных
                this.value = '';
                return;
            }

            // Дополнительная проверка для шаблона
            if (selectedFormat === 'docTemplate') {
                const newUsersInput = document.querySelector('[name="new_users"]');
                if (!newUsersInput.value.trim() || parseInt(newUsersInput.value) === 0) {
                    newUsersInput.style.borderColor = 'red';
                    const errorContainer = document.getElementById('error-container');
                    errorContainer.innerHTML = `
                        <div class="error-message" style="color: red; text-align: center;">
                            Для выгрузки шаблона необходимо указать количество новых пользователей
                        </div>
                    `;
                    this.value = '';
                    return;
                }
            }

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
                        throw new Error(`HTTP error! status: ${response.status}`);
                    });
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                const extension = selectedFormat === 'docTemplate' ? 'docx' : selectedFormat;
                a.download = `file.${extension}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                
                // Сбрасываем значение select после скачивания
                this.value = '';
            })
            .catch(error => {
                console.error('Ошибка при отправке данных:', error);
                // Сбрасываем значение select также в случае ошибки
                this.value = '';
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