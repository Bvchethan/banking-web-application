const currencyFormatter = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 2
});

const numberFormatter = new Intl.NumberFormat("en-IN");

export function formatCurrency(value) {
  const amount = Number(value ?? 0);
  return currencyFormatter.format(Number.isNaN(amount) ? 0 : amount);
}

export function formatNumber(value) {
  const amount = Number(value ?? 0);
  return numberFormatter.format(Number.isNaN(amount) ? 0 : amount);
}

export function formatDateTime(value) {
  if (!value) {
    return "--";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
}

export function maskAccountNumber(value) {
  if (!value) {
    return "--";
  }
  return String(value);
}

export function titleCase(value) {
  if (!value) {
    return "--";
  }

  return String(value)
    .toLowerCase()
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}
