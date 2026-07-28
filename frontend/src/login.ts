const login: HTMLFormElement | null = document.querySelector("form[name=login]");
if (login != null) {
  login.addEventListener("submit", () => {
    const username: HTMLInputElement | null =
      document.querySelector("input[name=username]");
    if (username != null) {
      // Usernames are ASCII, but the field is often filled from a Persian
      // keyboard or pasted with invisible marks. Stripping everything outside
      // ASCII is deliberate, so the control-character rule does not apply.
      const ascii = (username.value || "").split("@")[0].toLowerCase();
      // biome-ignore lint/suspicious/noControlCharactersInRegex: intentional non-ASCII strip
      username.value = ascii.replace(/[^\x00-\x7F]/g, "");

      window.console.log(username.value);
    }
  });
}
