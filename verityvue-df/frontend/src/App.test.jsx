import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import React from 'react'
import App from './App.jsx'

describe('App', () => {
	it('renders stream header', () => {
		render(<App />)
		expect(screen.getByText(/VerityVue — Stream/)).toBeInTheDocument()
	})
})
