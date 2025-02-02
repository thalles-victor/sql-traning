DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns
      WHERE table_name = 'brand' AND column_name = 'dsecription') THEN
    ALTER TABLE "brand" RENAME COLUMN "dsecription" TO "description";
  END IF;
END $$;