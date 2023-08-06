/**
 * @projectDescription publiquiz_flashcard.js
 * Plugin jQuery for quiz flashcard.
 *
 * @author Patrick PIERRE
 * @version 0.1
 */

/*jshint globalstrict: true*/
/*global jQuery: true */


"use strict";


/******************************************************************************
 *
 *                                  Flashcard
 *
 *****************************************************************************/

jQuery(document).ready(function($) {

    $(".pquizFlashcardContainer").each(function() {
        var prefix = $.publiquiz.defaults.prefix;
        var $container = $(this);
        var $flashcard = $container.find("."+prefix+"Flashcard");
        var $turnOverButton = $container.parent()
            .find("."+prefix+"FlashcardTurnOver ."+prefix+"Button");
        var $quizButtons = $container.parents("div[data-engine]")
            .parent().find("."+prefix+"Buttons");

        $turnOverButton.click(function() {
            if (!$turnOverButton.data("inProgress")) {
                $turnOverButton.data("inProgress", true);
                $quizButtons.find("."+prefix+"Submit").show();
                $turnOverButton.addClass("disabled");
                $flashcard.toggleClass("flipped");
            } else if ($quizButtons.find("."+prefix+"Score").is(":visible")) {
                $flashcard.toggleClass("flipped");
            }
        });

        $quizButtons.find("."+prefix+"Submit").hide().click(function() {
            $turnOverButton.removeClass("disabled"); });

        $quizButtons.find("."+prefix+"Redo")
            .click(function() {
                $turnOverButton.data("inProgress", false);
                $flashcard.removeClass("flipped");
            });
   });

});
