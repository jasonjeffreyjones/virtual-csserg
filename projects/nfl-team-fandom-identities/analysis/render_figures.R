#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  stop("Usage: render_figures.R RESULTS_JSON OUTPUT_DIRECTORY")
}
if (!requireNamespace("jsonlite", quietly = TRUE)) {
  stop("The jsonlite R package is required")
}

result_path <- args[[1]]
output_directory <- args[[2]]
dir.create(output_directory, recursive = TRUE, showWarnings = FALSE)
result <- jsonlite::fromJSON(result_path)

forest <- "#18352b"
artichoke <- "#4b6f44"
laurel <- "#dde3d8"
paper <- "#f6f4ed"
muted <- "#56635e"

png(
  file.path(output_directory, "happy-prevalence.png"),
  width = 1600,
  height = 1000,
  res = 200,
  bg = paper,
  type = "cairo"
)
par(mar = c(8, 5, 4, 1), fg = forest, col.axis = forest, col.lab = forest)
prevalence <- 100 * c(
  result$estimates$happy_prevalence_fandom_yes,
  result$estimates$happy_prevalence_fandom_no
)
bars <- barplot(
  prevalence,
  names.arg = c("Browns fan: Yes", "Browns fan: No"),
  col = c(artichoke, forest),
  border = NA,
  ylim = c(0, 100),
  ylab = "Endorsing happy (%)",
  main = "Happy endorsement and Browns fandom",
  cex.names = 1.05
)
abline(h = seq(0, 100, 20), col = laurel, lwd = 1)
rect(bars - 0.5, 0, bars + 0.5, prevalence, col = c(artichoke, forest), border = NA)
text(bars, prevalence + 4, sprintf("%.2f%%", prevalence), col = forest, font = 2)
text(
  bars,
  prevalence - 5,
  sprintf("n = %s", c(result$estimates$fandom_yes_n, result$estimates$fandom_no_n)),
  col = paper
)
mtext(
  sprintf(
    "Unweighted prevalence ratio %.3f; respondent-cluster bootstrap 95%% CI %.3f–%.3f",
    result$estimates$prevalence_ratio,
    result$estimates$cluster_bootstrap$prevalence_ratio_ci[[1]],
    result$estimates$cluster_bootstrap$prevalence_ratio_ci[[2]]
  ),
  side = 1,
  line = 4.5,
  cex = 0.85,
  col = muted
)
mtext(sprintf("Difference %+.2f percentage points (95%% CI %+.2f to %+.2f)",
  100 * result$estimates$prevalence_difference,
  100 * result$estimates$cluster_bootstrap$prevalence_difference_ci[[1]],
  100 * result$estimates$cluster_bootstrap$prevalence_difference_ci[[2]]),
  side = 1, line = 5.7, cex = 0.8, col = muted)
mtext(sprintf("%s to %s | %s respondents | Unweighted respondent-days",
  result$join_audit$earliest_eligible_obs_date,
  result$join_audit$latest_eligible_obs_date,
  format(result$join_audit$eligible_unique_respondents, big.mark = ",")),
  side = 1, line = 6.8, cex = 0.75, col = muted)
dev.off()

monthly <- result$temporal_sensitivity$by_month
month_dates <- as.Date(paste0(monthly$month, "-01"))
png(
  file.path(output_directory, "monthly-prevalence-ratio.png"),
  width = 1800,
  height = 1000,
  res = 200,
  bg = paper,
  type = "cairo"
)
par(mar = c(6, 5, 4, 1), fg = forest, col.axis = forest, col.lab = forest)
plot(
  month_dates,
  monthly$prevalence_ratio,
  type = "o",
  lwd = 2,
  pch = 21,
  cex = 0.8 + monthly$fandom_yes_n / max(monthly$fandom_yes_n),
  col = forest,
  bg = artichoke,
  xaxt = "n",
  xlab = "Month",
  ylab = "Monthly prevalence ratio",
  ylim = c(0.9, 1.25),
  main = "Monthly estimates fluctuate around the pooled result"
)
axis(1, at = month_dates, labels = monthly$month, las = 2, cex.axis = 0.8)
abline(h = 1, lty = 2, col = muted)
abline(h = result$estimates$prevalence_ratio, lty = 3, col = artichoke, lwd = 2)
legend(
  "bottomleft",
  legend = c("Monthly estimate", "Equal prevalence", "Pooled estimate"),
  lty = c(1, 2, 3),
  pch = c(21, NA, NA),
  pt.bg = c(artichoke, NA, NA),
  col = c(forest, muted, artichoke),
  bty = "n",
  cex = 0.8
)
mtext(
  "Point size reflects monthly Browns-fan respondent-days (15–29); monthly estimates are descriptive.",
  side = 1,
  line = 4.8,
  cex = 0.85,
  col = muted
)
dev.off()
