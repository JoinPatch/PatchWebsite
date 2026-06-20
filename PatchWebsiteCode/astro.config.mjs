// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  redirects: {
    '/impact-report': 'https://joinpatch.s3.eu-west-1.amazonaws.com/Patch+Demo+Day+2025+Impact+Report.pdf',
    '/2026-cohort': '/CohortBooks/Patch2026Cohort.pdf'
  }
});
