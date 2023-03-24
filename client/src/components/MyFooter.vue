<template>
  <footer class="footer">
    <div class="container">
      <p>&copy; {{ currentYear }} Hash Game Store </p>
    </div>
  </footer>
</template>

<script>
export default {
    
  data() {
    return {
      currentYear: new Date().getFullYear()
    };
  }
};
</script>

<style>
.footer {
  background-color: #f5f5f5;
  padding: 20px 0;
  text-align: center;
}
</style>
