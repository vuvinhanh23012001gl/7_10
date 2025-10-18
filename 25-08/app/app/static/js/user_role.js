export function set_user_or_admin(value) {
  sessionStorage.setItem("user", value ? "true" : "false");
}

export function get_user_or_admin() {
  if (sessionStorage.getItem("user") === null) {
    sessionStorage.setItem("user", "false");
  }
  return sessionStorage.getItem("user") === "true";
}