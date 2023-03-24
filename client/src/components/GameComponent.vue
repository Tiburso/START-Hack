<template>
  <div class="card-container">
    <div class="card">
      <slot></slot>
    </div>
  </div>
</template>

<style>
.card-container {
  display: flex;
  justify-content: flex-start;
  width: 50%;
}

.card {
  background-color: #ffffff;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  padding: 16px;
  margin: 16px;
  border-radius: 4px;
  width: 100%;
  height: 100%;
}
</style>
