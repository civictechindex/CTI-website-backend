# Update contributors

Searches GitHub for repositories with tags matching `civictechindex`, adds the new ones to the database, and creates new issues and project cards for their manual approval.

Uses the main Dockerfile in the repo and overrides the default CMD using args. See [action.yml](action.yml)

## Example usage

```yml
uses: ./.github/actions/update-contributors
env:
  POSTGRES_HOST: ${{ secrets.POSTGRES_HOST }}
  POSTGRES_PORT: 5432
  POSTGRES_DATABASE: ${{ secrets.POSTGRES_DATABASE }}
  POSTGRES_USER: ${{ secrets.POSTGRES_USER }}
  POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
  GH_TOKEN: ${{ secrets.GH_TOKEN }}
```
