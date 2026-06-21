// ... (Keep the rest of server.js the same, just locate the payload and regex loop inside app.post)

            const dataPayload = {
                fullName: fullName.toUpperCase(),
                currentName: currentName.toUpperCase(),
                birthDate: formattedDate, // Fixed: Named exactly birthDate to match your HTML
                matrixId: `_CORE_${metrics.hcv}_${metrics.life_path}`,
                
                // Calculated Metrics
                uspcScore: metrics.uspc_score,
                archetype: metrics.archetype,
                archSubtitle: archData.subtitle,
                archDesc: archData.description,
                archShadow: archData.shadow,
                archStrategy: archData.strategy,
                
                // Technical Grid Values
                lifePath: metrics.life_path,
                lifePathTitle: lpProfile,
                expression: metrics.expression,
                subconscious: metrics.subconscious_num,
                hcv: metrics.hcv,
                alignment: metrics.alignment_coefficient
            };

            // Load HTML Template and inject mapped payload tokens cleanly
            const templatePath = path.join(__dirname, 'report-template.html');
            let htmlResponse = fs.readFileSync(templatePath, 'utf8');

            // Strictly matches standard double curly braces: {{variable}}
            Object.keys(dataPayload).forEach(key => {
                const regex = new RegExp(`{{${key}}}`, 'g');
                htmlResponse = htmlResponse.replace(regex, dataPayload[key]);
            });

            res.send(htmlResponse);
