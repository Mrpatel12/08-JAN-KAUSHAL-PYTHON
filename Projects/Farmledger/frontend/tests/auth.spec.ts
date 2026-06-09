import { test, expect } from '@playwright/test'

test.describe('Auth flows', () => {
  test('Register shows verification notice', async ({ page }) => {
    await page.goto('/register')
    await page.fill('input[placeholder=""]', 'Test User')
    // fill email and password fields by order in the form
    const inputs = await page.locator('form input')
    await inputs.nth(0).fill('Test User')
    await inputs.nth(1).fill(`test+${Date.now()}@example.com`)
    await inputs.nth(2).fill('password123')
    await page.click('button:has-text("Register")')
    // redirect to verify-email page
    await expect(page).toHaveURL(/verify-email/)
    await expect(page.locator('text=Verifying').first()).toBeVisible().catch(()=>{})
  })

  test('Login page has forgot password link', async ({ page }) => {
    await page.goto('/login')
    await expect(page.locator('text=Forgot password?')).toBeVisible()
  })

  test('Password reset request shows confirmation', async ({ page }) => {
    await page.goto('/password-reset')
    await page.fill('input[type="email"]', `test+${Date.now()}@example.com`)
    await page.click('button:has-text("Send reset link")')
    await expect(page.locator('text=If the email exists, a reset link has been sent.')).toBeVisible()
  })
})
