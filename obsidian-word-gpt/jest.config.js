/** @type {import('jest').Config} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  collectCoverage: true,
  collectCoverageFrom: ['src/api.ts'],
  coverageThreshold: {
    global: {
      lines: 80,
      statements: 80,
      branches: 50,
      functions: 80,
    },
  },
};
