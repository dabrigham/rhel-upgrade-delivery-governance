# Deployment Recommendation

Recommended MVA:

1. Use Brigham Workflow Systems or Derek's personal site as the polished front
   door.
2. Use GitHub as the evidence layer.
3. Use LinkedIn Featured for distribution.

This avoids new paid hosting and keeps the public proof simple.

## Static Page

The publishable static bundle is in:

```text
web/
```

Preview locally:

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory web
```

Then open the local page in a browser. The `--bind 127.0.0.1` option keeps the
preview server bound to the local machine only.

The `web/` folder is self-contained for static publishing. Local links and image
assets are checked by:

```bash
./scripts/verify_public_export.sh
```

## GitHub Pages Option

If a standalone public proof page is needed, this repository can later be hosted
with GitHub Pages after approval. Do not publish until the sanitized content is
approved.

## Clean Public Export

The current local staging git history is not intended to be pushed publicly
because local scanner terms previously existed in that history. When Derek
approves publication, create a fresh public export directory with no `.git`
history:

1. Run `./scripts/verify_public_export.sh`.
2. Create a new empty export folder outside this staging repo.
3. Copy only publication-safe files into it, excluding `.git`,
   `scripts/sensitive_terms.local.txt`, caches, and generated demo outputs.
4. Confirm the exported folder contains `scripts/sensitive_terms.example.txt`
   but not `scripts/sensitive_terms.local.txt`.
5. Run the verifier again from the clean export folder.
6. Initialize a new public git repository only after the clean export passes and
   publication is explicitly approved.

## Suggested Slug

```text
rhel-upgrade-delivery-governance
```

## Stable URL Field

Once published, store the final URL in the job-search system as:

```text
case_study_url
```
