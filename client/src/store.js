export const store = {
  state: {
    thisUser: null,
    isLoggedIn: false
  },
  addNumber(newNumber) {
    this.state.numbers.push(newNumber);
  }
};
