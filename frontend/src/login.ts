let login: HTMLFormElement | null = document.querySelector("form[name=login]");
if (login != null) {
  login.addEventListener("submit", () => {
    let username: HTMLInputElement | null = document.querySelector(
      "input[name=username]"
    );
    if (username != null) {
      username.value = (username.value || "")
        .split("@")[0]
        .toLowerCase()
        .replace(/[^\x00-\x7F]/g, "");

      window.console.log(username.value);
    }
  });
}
