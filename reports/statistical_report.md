# IPL Statistical Validation Report

## 1. Toss Winner and Match Winner
**Finding tested:** Does winning the toss increase the probability of winning the match?
**Null hypothesis (H₀):** The toss winner wins 50% of decisive matches.
**Alternative hypothesis (H₁):** The toss winner's win rate is different from 50%.
**Test used:** One-sample binomial test
**Sample:** 1,187 decisive matches
**Result:** The toss winner won 613 matches (51.64%).
**p-value:** 0.2700
**95% confidence interval:** 48.80% to 54.48%
**Statistical verdict:** Fail to reject H₀ at α = 0.05.
**Plain-English interpretation:** Across the decisive matches analysed, the toss winner won 51.64% of matches. The 95% confidence interval includes 50%, and the result is not statistically significant. Therefore, any overall advantage from winning the toss is too small to distinguish from chance in this sample.

## 2. Toss Decision and Match Result

**Finding tested:** Does the decision made after winning the toss relate to whether the toss winner wins the match?
**Null hypothesis (H₀):** Toss decision and match outcome are independent.
**Alternative hypothesis (H₁):** Toss decision and match outcome are associated.
**Test used:** Chi-square test of independence
**Results:**
- Chose to bat: 184 wins out of 402 (45.8%)
- Chose to field: 429 wins out of 785 (54.6%)
**Test statistic:** χ² = 8.0401, df = 1
**p-value:** 0.0046
**Practical effect:** Toss winners who chose to field had a win rate about 8.8 percentage points higher than those who chose to bat (54.6% vs 45.8%).
**Statistical verdict:** Reject H₀ at α = 0.05.
**Plain-English interpretation:** The decision made after winning the toss is significantly associated with the match result. Toss winners who chose to field were more likely to win than those who chose to bat.

## 3. First-Innings Total: Defended vs Chased Down

**Finding tested:** Do successfully defended first-innings totals differ from totals that were successfully chased?
**Null hypothesis (H₀):** The mean first-innings total is the same for defended and chased-down matches.
**Alternative hypothesis (H₁):** The mean first-innings totals are different.
**Test used:** Welch's independent-samples t-test
**Results:**
- Defended matches: n = 540, mean first-innings total = 183.3
- Chased-down matches: n = 647, mean first-innings total = 155.5
- Mean difference ≈ 27.8 runs
**Test statistic:** t = 15.73
**p-value:** ≈ 1.2 × 10^-50
**Effect size:** Cohen's d = 0.916 (large effect)
**Statistical verdict:** Reject H₀ at α = 0.05.
**Plain-English interpretation:** Successfully defended first-innings totals were about 28 runs higher on average than totals that were chased down. The difference is statistically significant and the effect size is large, indicating a substantial practical difference between the two groups.

## 4. Bowling Type and Economy Rate

**Finding tested:** Does bowling economy rate differ across bowling types?
**Null hypothesis (H₀):** The mean economy rate is equal across all bowling-type groups.
**Alternative hypothesis (H₁):** At least one bowling-type group has a different mean economy rate.
**Test used:** One-way ANOVA
**Results:**
- Fast: mean economy rate = 8.647
- Medium: mean economy rate = 8.752
- Medium-fast: mean economy rate = 8.736
- Spin: mean economy rate = 7.983
- Total qualified bowlers = 277
**Test statistic:** F = 13.445
**p-value:** ≈ 3.3 × 10^-8
**Statistical verdict:** Reject H₀ at α = 0.05.
**ANOVA interpretation:** There is a statistically significant difference in mean economy rate among the bowling-type groups. ANOVA alone does not identify which specific group is responsible for the difference. Inspection of the group means suggests that spin bowlers drive the result because the three pace-group means are very similar while the spin mean is lower.

### Pace vs Spin Follow-up
The bowling types were then collapsed into pace and spin groups.
- Spin: n = 93, mean economy rate = 7.983
- Pace: n = 184, mean economy rate = 8.723
**Test used:** Welch's independent-samples t-test
**Test statistic:** t = -6.76
**p-value:** ≈ 1.3 × 10^-10
**Effect size:** Cohen's d = 0.807 (large effect)
**Statistical verdict:** Reject H₀ at α = 0.05.
**Plain-English interpretation:** Spin bowlers had a lower average economy rate than pace bowlers among the qualified bowlers analysed. The difference was statistically significant and had a large effect size.

## 5. Season Year and Average Match Scoring

**Finding tested:** Has average combined match scoring changed across IPL seasons?
**Null hypothesis (H₀):** There is no linear relationship between season year and average combined runs per match (r = 0).
**Alternative hypothesis (H₁):** There is a linear relationship between season year and average combined runs per match (r ≠ 0).
**Test used:** Pearson correlation
**Sample:** 19 IPL seasons
**Test statistic / Effect size:** Pearson r = 0.8610
**Coefficient of determination:** r² = 0.7413
**p-value:** ≈ 0.0000022
**Statistical verdict:** Reject H₀ at α = 0.05.
**Plain-English interpretation:** There is a strong positive relationship between season year and average combined runs per match. Later IPL seasons generally show higher scoring. Approximately 74.1% of the variation in season-level average scoring is associated with the linear relationship with season year.
**Important limitation:** Correlation does not establish causation. The increase in scoring may also be influenced by factors such as rule changes, pitch and boundary trends, bat technology, and changes in the mix of venues.

## 6. Venue and Chase Outcome

**Finding tested:** Do chase outcomes differ across the eight best-sampled venues?
**Null hypothesis (H₀):** Venue and chase outcome are independent.
**Alternative hypothesis (H₁):** Venue and chase outcome are associated.
**Test used:** Chi-square test of independence
**Sample:** 677 matches across the eight best-sampled venues
**Test statistic:** χ² = 6.7552, df = 7
**p-value:** 0.4548
**Statistical verdict:** Fail to reject H₀ at α = 0.05.
**Practical-significance comment:** Although individual venue chase rates showed visible differences — including a 65.2% chase win rate at Sawai Mansingh Stadium — the overall venue differences were not statistically distinguishable from chance in this sample.
**Plain-English interpretation:** The data does not provide sufficient evidence that chase outcome is associated with venue across these eight venues. This does not prove that venue has no effect; it means that this sample did not provide sufficient evidence to detect an association.

## 7. Powerplay vs Middle-Overs Scoring

**Finding tested:** Is there a meaningful difference in scoring between Powerplay and Middle-over deliveries?

**Null hypothesis (H₀):** The mean scoring per delivery is the same in the Powerplay and Middle overs.
**Alternative hypothesis (H₁):** The mean scoring per delivery differs between the Powerplay and Middle overs.
**Test used:** Welch's independent-samples t-test
**Sample:**
- Powerplay deliveries: n = 90,390
- Middle-over deliveries: n = 132,173
- Total: n = 222,563
**Test statistic:** t = 1.1206
**p-value:** 0.2625
**Effect size:** Cohen's d = 0.005 (approximately zero)
**Statistical verdict:** Fail to reject H₀ at α = 0.05.
**Plain-English interpretation:** The difference in scoring between Powerplay and Middle-over deliveries was not statistically significant, and the effect size was approximately zero. Despite the very large sample, there is no evidence here of a meaningful difference between the two groups.

## 8. Batting Handedness and Strike Rate

**Finding tested:** Do left-handed and right-handed qualified batters differ in mean strike rate?

**Null hypothesis (H₀):** Left-handed and right-handed qualified batters have the same mean strike rate.
**Alternative hypothesis (H₁):** Left-handed and right-handed qualified batters have different mean strike rates.
**Test used:** Welch's independent-samples t-test
**Sample:** 181 qualified batters
- Left-handed: n = 63, mean strike rate = 137.50
- Right-handed: n = 118, mean strike rate = 134.50
**Test statistic:** t = 1.1525
**p-value:** 0.2512
**Effect size:** Cohen's d = 0.178 (small effect)
**Statistical verdict:** Fail to reject H₀ at α = 0.05.
**Plain-English interpretation:** Left-handed qualified batters had a slightly higher average strike rate than right-handed qualified batters, but the difference was not statistically significant and the effect size was small. Therefore, this sample does not provide sufficient evidence of a meaningful difference in strike rate between left-handed and right-handed qualified batters.
**Unit-of-analysis note:** The batter, rather than the individual ball, is the appropriate unit for this question because the question compares hitters. Treating every ball as an independent observation would artificially inflate the sample size.

## Sample Size and Effect Size

A large sample does not automatically make every result statistically significant. Sample size affects how precisely an effect can be detected, while effect size describes how large the observed difference is in practical terms.
In the Powerplay-versus-Middle-over comparison, 222,563 deliveries were analysed, but the result was not statistically significant (p = 0.2625) and the effect size was approximately zero (Cohen's d = 0.005).
In contrast, the defended-versus-chased comparison showed a very strong statistical result (p ≈ 1.2 × 10^-50) and a large effect size (Cohen's d = 0.916), with defended first-innings totals averaging about 28 runs higher.
Therefore, p-values should not be interpreted alone. Statistical significance should be considered together with effect size and practical significance.
