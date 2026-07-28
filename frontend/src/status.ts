// Everything the status page used to run from inline <script> blocks in
// templates/status.html: the byte formatter, the per-package gauges and the
// 30-day usage chart.
//
// The template now emits its data once as JSON in a
// <script type="application/json" id="status-data"> tag, which the browser does
// not execute, and this module reads it. That keeps the logic type-checked and
// linted instead of living as untyped strings inside Jinja, and leaves the page
// free of executable inline script.
import {
  BarController,
  BarElement,
  CategoryScale,
  Chart,
  Legend,
  LinearScale,
  Tooltip,
  type TooltipItem,
} from "chart.js";
import Gauge from "svg-gauge/dist/gauge.min.js";

// Registered explicitly rather than importing "chart.js/auto", which pulls in
// every controller (line, radar, doughnut, polar, bubble, scatter) for what is
// a single stacked bar chart. Anything the chart starts using -- another scale,
// another plugin -- has to be added here, or Chart.js throws at runtime.
Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const FONT_FAMILY = "'Vazirmatn FD'";

interface StatusPackage {
  type: string;
  usage: string;
  total: string;
  percent: number;
}

interface StatusHistory {
  labels: string[];
  usage: number[];
  discount: number[];
}

interface StatusData {
  packages: StatusPackage[];
  history: StatusHistory;
}

const UNITS = [
  "کیلوبایت",
  "مگابایت",
  "گیگابایت",
  "ترابایت",
  "PiB",
  "EiB",
  "ZiB",
  "YiB",
];

/**
 * Format a byte count for the chart axis and tooltips.
 *
 * This deliberately does NOT match `bytes_to_str` in
 * internet/accounting/usage.py, even though the two look alike. The Python one
 * renders "-" below a kilobyte and uses "پتا بایت" as its fifth unit; this one
 * renders "0 مگابایت" and switches to PiB/EiB/ZiB/YiB. Those differences are
 * visible on the page, so the behaviour is preserved verbatim here rather than
 * quietly unified -- merging them is a product decision, not a refactor.
 */
export function humanFileSize(bytes: number): string {
  const thresh = 1024;

  if (Number.isNaN(bytes)) {
    return "∞";
  }
  if (Math.abs(bytes) < thresh) {
    return "0 مگابایت";
  }

  let value = bytes;
  let u = -1;
  do {
    value /= thresh;
    ++u;
  } while (Math.abs(value) >= thresh && u < UNITS.length - 1);

  if (u < 2 || (value * 10) % 10 === 0) {
    return `${value.toFixed(0)} ${UNITS[u]}`;
  }
  return `${value.toFixed(1)} ${UNITS[u]}`;
}

function readStatusData(): StatusData | null {
  const node = document.getElementById("status-data");
  if (node?.textContent == null) {
    return null;
  }
  return JSON.parse(node.textContent) as StatusData;
}

function renderGauges(packages: StatusPackage[]): void {
  for (const pkg of packages) {
    const element = document.getElementById(`package-${pkg.type}`);
    if (element == null) {
      continue;
    }
    const gauge = Gauge(element, {
      max: 100,
      label: () => `${pkg.usage} / ${pkg.total}`,
      value: 0,
    });
    gauge.setValueAnimated(pkg.percent, 1);
  }
}

function renderUsageChart(history: StatusHistory): void {
  const canvas = document.getElementById("usageChart");
  if (canvas == null) {
    return;
  }

  new Chart(canvas as HTMLCanvasElement, {
    type: "bar",
    data: {
      labels: history.labels,
      datasets: [
        {
          label: "میزان مصرف ثبت شده",
          data: history.usage,
          backgroundColor: "rgba(31,119,180,0.8)",
        },
        {
          label: "میزان مصرف تخفیف خورده",
          data: history.discount,
          backgroundColor: "rgba(254,127,14,0.8)",
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          mode: "index",
          intersect: false,
          bodyFont: { family: FONT_FAMILY },
          footerFont: { family: FONT_FAMILY },
          callbacks: {
            // Text for an individual item in the tooltip.
            label: (context: TooltipItem<"bar">) =>
              humanFileSize(context.raw as number),
            // Footer is shared by both datasets, so it shows their total.
            footer: (items: TooltipItem<"bar">[]) =>
              humanFileSize(items.reduce((sum, item) => sum + (item.raw as number), 0)),
          },
        },
        legend: {
          labels: { font: { family: FONT_FAMILY } },
        },
      },
      scales: {
        y: {
          stacked: true,
          ticks: {
            callback: (label) => humanFileSize(label as number),
            font: { family: FONT_FAMILY },
          },
        },
        x: {
          stacked: true,
          ticks: { font: { family: FONT_FAMILY } },
        },
      },
    },
  });
}

const data = readStatusData();
if (data != null) {
  renderGauges(data.packages);
  renderUsageChart(data.history);
}
