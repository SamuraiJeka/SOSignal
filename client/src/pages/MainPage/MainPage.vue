<template>
  <v-container class="pa-4">
    <!-- Заголовок и кнопка заказа помощи -->
    <v-row align="center" justify="space-between">
      <v-col>
        <h1>Ваши поездки</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" @click="dialog = true">
          Заказать помощь
        </v-btn>
      </v-col>
    </v-row>

    <!-- Единая таблица поездок или сообщение об отсутствии -->
    <v-row>
      <v-col cols="12">
        <div v-if="trips.length === 0" class="text-center my-12">
          <h3>У вас пока нет поездок</h3>
        </div>
        <v-card v-else>
          <v-data-table
            :headers="headers"
            :items="trips"
            class="elevation-1"
            dense
          >
            <template #header.{ header }>
              <span v-text="header.title" />
            </template>
            <template #item.date="{ item }">
              {{ formatDate(item.date) }}
            </template>
            <template #item.isComplete="{ item }">
              <v-chip :color="item.isComplete ? 'grey' : 'blue'" dark>
                {{ item.isComplete ? 'Завершено' : 'В процессе' }}
              </v-chip>
            </template>
            <template #item.actions="{ item }">
              <v-btn
                v-if="!item.isComplete"
                color="success"
                small
                @click="finishTrip(item)"
              >
                Окончить
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Модалка заказа помощи -->
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title class="headline">Заказать помощь</v-card-title>
        <v-card-text>
          <v-form ref="formRef" v-model="formValid">
            <v-text-field
              v-model="form.date"
              label="Дата"
              type="date"
              :rules="[v => !!v || 'Выберите дату']"
              required
            />
            <v-checkbox
              v-model="form.hasLuggage"
              label="Есть ли багаж"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" :disabled="!formValid" @click="addTrip">
            Заказать
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

// Данные поездок
const trips = ref([]);

// Состояние формы
const dialog = ref(false);
const form = ref({ date: '', hasLuggage: false });
const formValid = ref(false);
const formRef = ref(null);

// Заголовки таблицы с возможностью сортировки
const headers = [
  { title: 'Дата', key: 'date', sortable: true },
  { title: 'Персонал', key: 'stuff', sortable: true },
  { title: 'Статус', key: 'isComplete', sortable: true },
  { title: 'Действия', key: 'actions', sortable: false }
];

// Форматирование даты
function formatDate(d) {
  return new Date(d).toLocaleDateString('ru-RU');
}

// Добавление новой поездки
function addTrip() {
  if (formRef.value.validate()) {
    trips.value.push({
      date: form.value.date,
      stuff: form.value.hasLuggage ? 1 : 0,
      isComplete: false
    });
    form.value = { date: '', hasLuggage: false };
    dialog.value = false;
  }
}

// Завершение поездки
function finishTrip(item) {
  item.isComplete = true;
}
</script>

<style scoped>
.text-center {
  text-align: center;
}
.my-12 {
  margin-top: 3rem;
  margin-bottom: 3rem;
}
</style>
