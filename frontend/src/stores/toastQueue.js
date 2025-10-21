import { defineStore } from 'pinia';
import { useToast } from 'vue-toast-notification';

export const useToastQueueStore = defineStore('toastQueue', () => {
  const toast = useToast();
  let queue = [];
  let active = false;

  function showNext() {
    if (queue.length === 0) {
      active = false;
      return;
    }
    active = true;
    const { message, options } = queue.shift();
    toast.open({
      message,
      ...options,
      onClose: () => {
        showNext();
      }
    });
  }

  function enqueue(message, options = {}) {
    queue.push({ message, options });
    if (!active) {
      showNext();
    }
  }

  return { enqueue };
});

// Usage example:
// const toastQueue = useToastQueueStore();
// toastQueue.enqueue('This is a toast message', { type: 'success', duration: 3000 });